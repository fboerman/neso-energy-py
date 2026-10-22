import requests
import json

__title__ = "neso-energy-py"
__version__ = "0.1.0"
__author__ = "Frank Boerman-Lima"
__license__ = "MIT"


class NesoRawClient:
    BASE_URL = "https://api.neso.energy"

    def __init__(self, api_key: str = None, proxies: dict = None):
        self.s = requests.Session()
        self.s.headers.update({
            'user-agent': 'neso-py',
            'Content-Type': 'application/json'
        })

        if proxies is not None:
            # proxies should be defined as mandated by the requests library: https://requests.readthedocs.io/en/latest/user/advanced/#proxies
            self.s.proxies.update(proxies)

        self.DATASETS = self._update_data_sets()


    def _update_data_sets(self):
        r = self.s.get(self.BASE_URL + '/api/3/action/package_list')
        r.raise_for_status()
        return r.json()['result']

    def query_tables_from_set_name(self, data_set: str):
        if data_set not in self.DATASETS:
            raise Exception('Invalid data set!')

        r = self.s.get(self.BASE_URL + '/api/3/action/datapackage_show', params={
            'id': data_set
        })
        r.raise_for_status()
        return r.json()['result']

    def get_resource_info(self, resource_id):
        r = self.s.get(self.BASE_URL + '/api/3/action/resource_show', params={
            'id': resource_id
        })
        r.raise_for_status()
        return r.json()['result']

    def get_resource_csv_by_path(self, path):
        r = self.s.get(path)
        r.raise_for_status()
        return r.content

    def get_resource_csv_path_by_id(self, resource_id):
        return self.get_resource_info(resource_id)['path']

    def query_resource(self, sql):
        r = self.s.get(self.BASE_URL + '/api/3/action/datastore_search_sql', params={
            'sql': sql
        })
        r.raise_for_status()
        data = r.json()
        if not data.get("success"):
            err = data.get("error", {})
            if "sql" in err:
                sql_err = err["sql"]
                error_msg = sql_err[0] if isinstance(sql_err, list) else sql_err
                raise Exception(f"SQL/Database Error: {error_msg}")
            if "message" in err:
                raise Exception(f"Error ({err.get('__type')}): {err['message']}")
            raise Exception(f"CKAN Error: {json.dumps(err, indent=2)}")
        return data['result']['records']

    def query_resource_by_id(self, resource_id, filter=None):
        # this is a helper function for common select * from table where <filter>
        return self.query_resource(
            sql=f'''select * from "{resource_id}" {"WHERE " + filter if filter is not None else ""} order by "_id" ASC '''
        )
