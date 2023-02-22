import uvicorn
from services.fastapi_template.main import factory

app = factory()

if __name__ == '__main__':
    uvicorn.run(
        'fastapi_template:app', host='0.0.0.0', port=8010, reload=True, debug=True, log_config='etc/logging.conf'
    )
