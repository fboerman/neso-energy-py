from nesoenergy import NesoClient
import pytest

@pytest.fixture()
def client():
    client = NesoClient()
    yield client


def test_demand_2025_csv(client):
    df = client.get_resource_csv_by_name(
        data_set='historic-demand-data',
        resource_name='historic_demand_data_2025'
    )

    assert len(df) == 17520
    assert len(df.columns) == 22

def test_demand_2025_query(client):
    df = client.query_resource_by_name(
        data_set='historic-demand-data',
        resource_name='historic_demand_data_2025',
        filter='"ENGLAND_WALES_DEMAND" > 30000'
    )

    assert len(df) == 2970
    assert len(df.columns) == 22
