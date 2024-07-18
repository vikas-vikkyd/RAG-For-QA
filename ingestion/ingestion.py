import os
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from load_data import load_data
from argparse import ArgumentParser

parser = ArgumentParser(description="Ingest data to Vector database")
parser.add_argument("--data_path", type=str, required=True, help="Path for documents")
parser.add_argument("--chunk_size", type=int, default=1000, help="Path for documents")
parser.add_argument(
    "--chunck_overlap_size", type=int, default=0, help="Path for documents"
)
parser.add_argument(
    "--collection_name", type=str, required=True, help="Path for documents"
)
args = parser.parse_args()


def data_reader(data_path):
    """Read data"""
    all_data = []
    # read all pdf files in provided directory
    for file in os.listdir(data_path):
        print("Processing started for file: ", file)
        reader = PdfReader(os.path.join(data_path, file))
        pages = reader.pages

        # add metadata for pages
        try:
            for i, page in enumerate(pages):
                data_dict = {
                    "file": file,
                    "page_number": i,
                    "page_content": page.extract_text(),
                }
                all_data.append(data_dict)
        except Exception as e:
            print("Not able to read content from file: ", file)
    return all_data


def create_chunk(data, chunk_size, chunck_overlap_size):
    """Create chunk"""
    # define splitter
    character_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunck_overlap_size,
    )
    all_data = []
    # loop over pages
    for data_dict in data:
        # create chunks
        texts = character_splitter.split_text(data_dict["page_content"])
        # create metadata for chunk
        for text in texts:
            data = {
                "file": data_dict["file"],
                "page_number": data_dict["page_number"],
                "page_content": text,
            }
            all_data.append(data)
    return all_data


def main():
    """Main module to ingest data"""
    # read data
    all_pages = data_reader(args.data_path)

    # create chunks
    all_chunks = create_chunk(all_pages, args.chunk_size, args.chunck_overlap_size)

    # load data to vector database
    load_data(all_chunks, args.collection_name)


if __name__ == "__main__":
    main()
