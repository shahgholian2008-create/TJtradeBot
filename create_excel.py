"""ساخت فایل users.xlsx با ساختار صحیح"""
import pandas as pd


def main():
    sheets_data = {}

    sheets_data["MAP_SRC"] = pd.DataFrame({
        "username": [f"MAP_SRC{''.join(__import__('random').choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))}" for _ in range(15)],
        "password": [''.join(__import__('random').choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10)) for _ in range(15)],
        "used": ["no"] * 15,
    })
    # ... بقیه شیت‌ها

    with pd.ExcelWriter("users.xlsx", engine="openpyxl") as writer:
        for name, df in sheets_data.items():
            df.to_excel(writer, sheet_name=name, index=False)

    print("✅ users.xlsx created.")


if __name__ == "__main__":
    main()