train:
	python3 src/train.py

mdl-exp:
	python3 src/export_model.py

build-mlflow:
	docker build -t mlflow-api .

run-mlflow:
	docker run -p 5001:5001 mlflow-api