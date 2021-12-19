
# Getting Started

## Clone Project

      git clone https://github.com/umutBayraktar/courier-path.git

## Install MongoDB
    https://docs.mongodb.com/manual/installation/


## Create Virtual Environment
    
Notice That! Python version should be 3.6 or upper

    virtualenv -p python3 env

## Install Requirements

activate environment 

    source env/bin/activate

go to path

    cd navigation

install requirements

    pip3 install -r requirements.txt

## Run Project

    cd src

    uvicorn main:app --reload

## Open Doc

    http://localhost:8000/docs