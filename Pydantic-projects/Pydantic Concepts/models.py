from pydantic import BaseModel, Field, field_validator, model_validator, computed_field, ConfigDict, EmailStr, AnyUrl
from typing import Optional, Literal
from datetime import date

class Category(BaseModel):
    name:Literal['starter', 'main_course', 'dessert', 'beverage']

# BaseModel is checking if the incoming data is valid or not, if not it will throw an error
# '...' needs to be used in the Field function to indicate that the field is required and must be provided when creating an instance of the model.

class Model(BaseModel):
    model_config = ConfigDict(
        #extra='forbid', # This will forbid any extra fields that are not defined in the model
        # extra='allow', # This will allow any extra fields that are not defined in the model
        extra='ignore', # This will ignore any extra fields that are not defined in the model
        frozen=True, # This will make the model immutable, meaning that the values of the fields cannot be changed after the model instance is created  
        # strict=True, # This will enforce strict type checking, meaning that the values of the fields must be of the correct type and cannot be coerced to the correct type
        strict=False, # This will allow coercion of the values of the fields to the correct type if possible
        validate_assignment=True, # This will validate the values of the fields when they are assigned to the model instance
    )
    
     
    #Field : Value Type
    id : int
    name : str = (Field(..., min_length=3, max_length=50, description="Name of the item")) # Required field with validation for minimum and maximum length
    price : float = (Field(..., gt=0, description="Price of the item")) # Required field with validation for greater than zero
    category : Category = (Field(..., description="Category of the item")) # Required field
    is_available : bool = (Field(default=True)) # Default value of True if not provided
    description : Optional[str] = None # Optional field with default value of None
    # email : EmailStr -> valid email
    # url : AnyUrl -> Valid url
    # Date : date -> Valid data format follow


    #field Validator : It is used to validate the field values before creating an instance of the model. It can be used to check if the value of a field meets certain criteria or to modify the value of a field before it is set.
    @field_validator('name')
    @classmethod
    def title_name(cls, vlaue):
        return vlaue.title() # This will convert the name of the item to title case before creating an instance of the model

    # Model Validation : It is used to validate the entire model before creating an instance of the model. It can be used to check if the values of multiple fields meet certain criteria or to modify the values of multiple fields before they are set.
    @model_validator(mode='after')
    def check_available(self):
        if self.is_available and self.price <= 0:
            raise ValueError("Price must be greater than zero if the item is available")
        return self

    # ComputedField : It is used to create a field that is computed based on the values of other fields. It can be used to create a field that is derived from the values of other fields or to create a field that is calculated based on the values of other fields.
    @computed_field
    @property
    def price_tax(self) -> float:
        return round(self.price * 1.1, 2) # This will calculate the price of the item with tax (10% tax) and return it as a computed field

item = Model(id=1, name='ESPRESSO', price=20.98, category=Category(name='beverage'), is_available=True)


#1. model_dump : It is used to convert the model instance to a dictionary. It can be used to convert the model instance to a dictionary for serialization or for other purposes.
# this will work only inside python
print("Dictionary representation of the model instance:")
print(item.model_dump()) # This will convert the model instance to a dictionary and print it

#2. model_dump_json : It is used to convert the model instance to a JSON string. It can be used to convert the model instance to a JSON string for serialization or for other purposes.
# Outside python, this will work in any language that can parse JSON
print("JSON representation of the model instance:")
print(item.model_dump_json()) # This will convert the model instance to a JSON string and print it
