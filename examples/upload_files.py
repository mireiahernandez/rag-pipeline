# Upload the ACME_Earnings.pdf file to the tenant1 database
import requests

if __name__ == "__main__":
    pdf_paths = [
        "examples/pdfs/Employee Handbook 2013-14.pdf",
        "examples/pdfs/ACME_Earnings.pdf"
    ]

    files = []
    for pdf_path in pdf_paths:
        files.append(
            (
                "files",
                (pdf_path.split("/")[-1], open(pdf_path, "rb"), "application/pdf")  # noqa: E501
            )
        )

    # db name is tenant1
    db_name = "test_tenant1"
    params = {
        "db_name": db_name
    }

    # Make the POST request with the list of files
    response = requests.post(
        "http://0.0.0.0:8000/upload/",
        files=files,
        params=params
    )

    print(response.json())

    # Close the files after the request
    for _, (filename, file, _) in files:
        file.close()  # Ensure each file is closed after the request
