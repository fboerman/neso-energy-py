import pandas as pd
import io
from .nesoraw import NesoRawClient


class NesoClient(NesoRawClient):
    CACHE = {
        'datasets': {},
        'resources_paths': {},
        'resources_ids': {}
    }
    def query_tables_from_set_name(self, data_set: str):
        if data_set in self.CACHE['datasets']:
            return self.CACHE['datasets'][data_set]
        df = pd.DataFrame(super().query_tables_from_set_name(data_set)['resources']).drop(columns=['hash'])
        self.CACHE['datasets'][data_set] = df
        self.CACHE['resources_paths'] |= dict(
            zip(
                df['id'],
                df['path']
            )
        )
        self.CACHE['resources_ids'] |= dict(
            zip(
                data_set + "/" + df['name'],
                df['id']
            )
        )
        return df

    def get_resource_id_by_name(self, data_set, resource_name):
        key = f'{data_set}/{resource_name.lower().replace(' ', '_')}'
        res_id = self.CACHE['resources_ids'].get(key, None)
        if res_id is None:
            self.query_tables_from_set_name(data_set)
            res_id = self.CACHE['resources_ids'].get(key, None)
            if res_id is None:
                raise Exception(f'Invalid resource {key}!')

        return res_id

    def get_resource_csv_by_path(self, path):
        return pd.read_csv(
            io.BytesIO(super().get_resource_csv_by_path(path))
        )

    def get_resource_csv_by_id(self, resource_id):
        path = self.CACHE['resources_paths'].get(
            resource_id,
            None
        )
        if path is None:
            path = super().get_resource_csv_path_by_id(resource_id)
            self.CACHE['resources_paths'][resource_id] = path
        return self.get_resource_csv_by_path(path)

    def get_resource_csv_by_name(self, data_set, resource_name):
        return self.get_resource_csv_by_id(
            self.get_resource_id_by_name(data_set, resource_name)
        )

    def query_resource(self, sql):
        return pd.DataFrame(
            super().query_resource(sql)
        ).drop(columns=['_id', '_full_text'])

    def query_resource_by_id(self, resource_id, filter=None):
        return pd.DataFrame(
            super().query_resource_by_id(resource_id, filter=filter)
        )

    def query_resource_by_name(self, data_set, resource_name, filter=None):
        return self.query_resource_by_id(
            self.get_resource_id_by_name(data_set, resource_name),
            filter=filter
        )
