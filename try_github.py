from github_client import GitHubError, fetch_pr

url = input("Paste a GitHub Pull Request URL: ")

try:
    pr = fetch_pr(url)

    print("\n--- PULL REQUEST DETAILS ---")
    print("Title:", pr["title"])
    print("Author:", pr["author"])
    print("Status:", pr["state"])
    print("Files changed:", pr["changed_files_count"])
    print("Additions:", pr["additions"])
    print("Deletions:", pr["deletions"])

    print("\n--- CHANGED FILES ---")

    for file in pr["files"]:
        print(
            file["filename"],
            "| Status:", file["status"],
            "| Has diff:", bool(file["patch"])
        )

except GitHubError as error:
    print("\nProblem:", error)
