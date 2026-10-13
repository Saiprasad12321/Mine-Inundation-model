import json
import pandas as pd

with open("data/extracted/inundation_incidents.json", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
print("=== VERIFICATION STATUS BREAKDOWN ===")
print(df["verification_status"].value_counts())

print("\n=== IS_VERIFIED_INUNDATION ===")
print(df["is_verified_inundation"].value_counts())

print("\n=== MINERAL / CATEGORY (VERIFIED ONLY) ===")
print(df[df["is_verified_inundation"]]["mineral"].value_counts())

print("\n=== REPORT TYPE (VERIFIED ONLY) ===")
print(df[df["is_verified_inundation"]]["report_type"].value_counts())

print("\n=== TOTAL FATALITIES BY CATEGORY ===")
print(df.groupby("verification_status")["fatalities"].sum())
