from typing import Any

import requests
import streamlit as st

from workflow_lab.config import settings

API_URL = f"{settings.URL_PREFIX}/workflow"


def run_workflow() -> int:
    """
    Executes the workflow through the API.

    Returns:
        Result produced by the workflow.

    Raises:
        requests.HTTPError:
            If the API request fails.
        TypeError:
            If the API response has an invalid format.
    """

    response = requests.post(API_URL, timeout=30)
    response.raise_for_status()

    payload: dict[str, Any] = response.json()
    result = payload.get("result")

    if not isinstance(result, int):
        raise TypeError("Invalid workflow response: expected integer result.")

    return result


st.set_page_config(
    page_title="Workflow Lab",
    page_icon="🧪",
)

st.title("Workflow Lab")
st.write("Run the baseline workflow.")

if st.button("Run Workflow"):
    with st.spinner("Working..."):
        try:
            result = run_workflow()
            st.json(result)
        except requests.RequestException as exc:
            st.error(f"Workflow request failed: {exc}")
