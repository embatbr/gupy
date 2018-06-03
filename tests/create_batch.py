from common import *


name = uuid.uuid4().hex
(mickey_first_name, mickey_last_name) = (name[ : random.randint(3, 5)],
                           name[random.randint(5, 10) : random.randint(15, 20)])

name = uuid.uuid4().hex
(donald_first_name, donald_last_name) = (name[ : random.randint(3, 5)],
                           name[random.randint(5, 10) : random.randint(15, 20)])


resp = r.post(
    'http://{host}:{port}/candidates'.format(**app_conn_settings),
    data={
        'file_data': base64.b64encode(open('./batch.zip', 'rb').read())
    }
)

print(resp)
print(resp.json())
