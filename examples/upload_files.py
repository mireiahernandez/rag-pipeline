# Upload the ACME_Earnings.pdf file to the tenant1 database
import requests

if __name__ == "__main__":
    # pdf_path = "examples/ACME_earnings/ACME_Earnings.pdf"
    pdf_path = "examples/Google_employee_handbook/Employee Handbook 2013-14.pdf"  # noqa: E501
    with open(pdf_path, "rb") as file:
        files = {
            "file": (
                pdf_path.split("/")[-1],
                file,
                "application/pdf"
            )
        }
        # db name is tenant1
        db_name = "test_tenant1"
        params = {
            "db_name": db_name
        }
        response = requests.post(
            "http://0.0.0.0:8000/upload/",
            files=files,
            params=params
        )
        print(response.json())
