from fastapi import FastAPI
from pydantic import BaseModel,Json
from typing import List, Union,Optional

					


class login_data(BaseModel):
	username:str
	password:str											




class updateSportsData(BaseModel):
	log_data: list




class uploadImageFile(BaseModel):
	Params :Json
