DATA_PATH=$1
COLLECTION_NAME=$2
python ingestion/ingestion.py \
	--data_path=${DATA_PATH} \
	--collection_name=${COLLECTION_NAME}