import argparse
import sqlite3
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://api.freeapi.app/api/v1/public/randomusers"

def extract_data(page: int | None = None, limit: int | None = None) -> dict:
	params = {}
	if page is not None:
		params["page"] = page
	if limit is not None:
		params["limit"] = limit

	response = requests.get(API_URL, params=params, timeout=30)
	response.raise_for_status()
	payload = response.json()

	if payload.get("statusCode") != 200:
		raise ValueError(f"Unexpected API response: {payload.get('statusCode')}")

	return payload["data"]


def transform_data(api_data: dict) -> pd.DataFrame:
	records = api_data.get("data", [])
	if not records:
		return pd.DataFrame()

	frame = pd.json_normalize(records)
	rename_map = {
		"name.title": "name_title",
		"name.first": "name_first",
		"name.last": "name_last",
		"location.street.number": "street_number",
		"location.street.name": "street_name",
		"location.city": "city",
		"location.state": "state",
		"location.country": "country",
		"location.postcode": "postcode",
		"location.coordinates.latitude": "latitude",
		"location.coordinates.longitude": "longitude",
		"location.timezone.offset": "timezone_offset",
		"location.timezone.description": "timezone_description",
		"login.uuid": "login_uuid",
		"login.username": "login_username",
		"login.password": "login_password",
		"login.salt": "login_salt",
		"login.md5": "login_md5",
		"login.sha1": "login_sha1",
		"login.sha256": "login_sha256",
		"dob.date": "dob_date",
		"dob.age": "dob_age",
		"registered.date": "registered_date",
		"registered.age": "registered_age",
		"picture.large": "picture_large",
		"picture.medium": "picture_medium",
		"picture.thumbnail": "picture_thumbnail",
	}
	frame = frame.rename(columns=rename_map)

	selected_columns = [
		"id",
		"gender",
		"name_title",
		"name_first",
		"name_last",
		"email",
		"phone",
		"cell",
		"nat",
		"street_number",
		"street_name",
		"city",
		"state",
		"country",
		"postcode",
		"latitude",
		"longitude",
		"timezone_offset",
		"timezone_description",
		"login_uuid",
		"login_username",
		"login_password",
		"dob_date",
		"dob_age",
		"registered_date",
		"registered_age",
		"picture_large",
		"picture_medium",
		"picture_thumbnail",
	]

	for column in selected_columns:
		if column not in frame.columns:
			frame[column] = None

	ordered_frame = frame[selected_columns].copy()
	ordered_frame["id"] = pd.to_numeric(ordered_frame["id"], errors="coerce")
	ordered_frame["dob_age"] = pd.to_numeric(ordered_frame["dob_age"], errors="coerce")
	ordered_frame["registered_age"] = pd.to_numeric(ordered_frame["registered_age"], errors="coerce")

	return ordered_frame


def load_data(frame: pd.DataFrame, page: int | None = None, limit: int | None = None) -> None:
	if frame.empty:
		print("No records returned from the API.")
		return

	frame = frame.copy()
	frame["source_page"] = page
	frame["source_limit"] = limit

	with sqlite3.connect(DB_PATH) as connection:
		frame.to_sql("random_users", connection, if_exists="append", index=False)

	print(f"Loaded {len(frame)} rows into {DB_PATH}")


def run_etl(page: int | None = None, limit: int | None = None) -> None:
	api_data = extract_data(page=page, limit=limit)
	transformed_data = transform_data(api_data)
	load_data(transformed_data, page=page, limit=limit)


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Run the random users ETL pipeline.")
	parser.add_argument("--page", type=int, default=None, help="Optional page number to fetch from the API.")
	parser.add_argument("--limit", type=int, default=None, help="Optional number of records to fetch from the API.")
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	run_etl(page=args.page, limit=args.limit)