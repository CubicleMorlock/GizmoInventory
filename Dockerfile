FROM python:3.13-bookworm

RUN mkdir /GizmoInventory
COPY requirements.txt /GizmoInventory

RUN pip3 install -r /GizmoInventory/requirements.txt

COPY inventory_app.py /GizmoInventory
COPY inventory.db /GizmoInventory
COPY app/ /GizmoInventory/app/

CMD ["python3", "/GizmoInventory/inventory_app.py"]
