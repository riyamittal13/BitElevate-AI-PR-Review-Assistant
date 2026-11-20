
import pytest

from github_client import GitHubError, parse_pr_url


def test_parse_valid_pr_url():
    url = "https://github.com/psf/requests/pull/7388"

    owner, repo, number = parse_pr_url(url)

    assert owner == "psf"
    assert repo == "requests"
    assert number == 7388


def test_parse_pr_url_with_trailing_slash():
    url = "https://github.com/psf/requests/pull/7388/"

    owner, repo, number = parse_pr_url(url)

    assert owner == "psf"
    assert repo == "requests"
    assert number == 7388


def test_invalid_pr_url():
    url = "https://github.com/psf/requests"

    with pytest.raises(GitHubError):
        parse_pr_url(url)
