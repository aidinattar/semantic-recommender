.PHONY: build embed query clean

# Compila il codice C++
build:
	cd src/recommender && cmake . && make

# Genera gli embedding
embed:
	python3 src/nlp/build_embeddings.py

# Esegue una query con embedding + motore
query:
	python3 src/nlp/query_example.py

# Pulisce tutto
clean:
	rm -rf src/recommender/CMakeFiles src/recommender/Makefile src/recommender/*.o
	rm -f embeddings/*.npy embeddings/*.csv



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Make dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) src/nlp/dataset.py


## Make requirements
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -r src/nlp/requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -r src/recommender/requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -r src/visualization/requirements.txt


## Make Embeddings
.PHONY: embeddings
embeddings: requirements
	$(PYTHON_INTERPRETER) src/nlp/build_embeddings.py build


## Make Query
.PHONY: query
query: requirements
	$(PYTHON_INTERPRETER) src/nlp/generate_query.py --query "$(QUERY)"


