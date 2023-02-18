

from django.forms import ModelForm
from django.db.models import Model
from typing import Union


def search_in_model(data: dict, field_names: list, model: Model) -> list:
    """La función busca un objeto en el modelo usando los campos y filtros dados y devuelve un array.

    La idea es que en el backend se especique los campos y los filtros permitidos para hacer la consulta en el modelo dado, y en el
    frontend se debe especificar los mismo nombres de campos.

    - data : es un json que viene del frontend y debe contener los mismo nombres de campos especificados en `field_names`
    - field_names : es una lista de nombres de campos que tiene la siguiente sintaxis: ["nombreDeCampo1__filtroDeDjango", "nombreDeCampo2"].
    Un ejempo más real seria: ["tipo_vehiculo", "placa__icontains"] indica que se filtrarán los resultados usando los campos 'tipo_vehiculo' y 'placa' y 
    el campo `placa` usa el filtro de consulta '__icontains' para no distinguir entre mayusculas y minuscula.

    """
    # Si los nombres de campos especificados en el backend y frontend no son los mismo se devuelve una lista vacia.
    for field in field_names:        
        if "__" in field:            
            name= field.split("__")[0]
        else:
            name= field        
        if data.get(name) is None:
            return []  
    
    # Organiza los datos para que el filtro especificado en el backend se aplique en la consulta.
    filter= {}
    for field in field_names:        
        if "__" in field:            
            name= field.split("__")[0]
            name_and_filter= field
            value= data.get(name)            
            filter.update({name_and_filter:value})
            continue
        value= data.get(field)
        filter.update({field:value})
    
    try:
        queryset = model.objects.filter(**filter)
        return list(queryset.values())
    except model.DoesNotExist:
        return []


def buscar_objeto(modelo: Union[Model, ModelForm], id_objeto) -> Union[Model, None]:
    """La función trata de encontrar un objeto específico del modelo dado, usando su id. 
    Si el objeto existe, la función devuelve el objeto. Si el objeto no existe, la función devuelve None.

    Args:
        Modelo: la Clase del modelo.
        id_objeto: el id que se buscará en la Clase del modelo.
    """
    try:
        if id_objeto == "":
            return None
        if issubclass(modelo, ModelForm):
            modelo = modelo.Meta.model
        objeto = modelo.objects.get(id=id_objeto)
        return objeto
    except modelo.DoesNotExist:
        return None


def checker(data: dict, form_model: ModelForm, keyname_model: str = None) -> Union[Model, dict]:
    """Si los datos proporcionados son validos devuelve una instancia del modelo dado, en caso contrario devuelve un dict con un mensaje de error:{keyname:msg}

    La función checker toma tres argumentos: 
    - data, 
    - form_model
    - ~keyname_model~. 
    La función se usa para verificar si el valor de un campo del formulario es válido y existe en la base de datos. 
    La función primero verifica si el valor de keyname_model está presente en el diccionario data y es un objeto JSON válido. 
    Si no es así, la función devuelve un diccionario con un mensaje de error indicando que el valor no está presente o no es un JSON válido.

    Si el objeto JSON tiene una clave "id", la función llama a buscar_objeto para buscar el objeto en la base de datos utilizando el modelo form_model. 
    Si el objeto no existe en la base de datos, 
    la función devuelve un diccionario con un mensaje de error indicando que el id del modelo no existe en la base de datos.

    Si el objeto JSON no tiene una clave "id", 
    la función intenta crear un nuevo objeto a partir de los datos proporcionados en el objeto JSON utilizando el modelo form_model. 
    Si el formulario es válido, la función devuelve el objeto creado. 
    Si el formulario no es válido, la función devuelve un diccionario con un mensaje de error que indica los problemas de validación.
    """
    objecto = None
    if keyname_model is None:
        keyname_model = form_model.Meta.model.__name__.lower()

    if not issubclass(form_model, ModelForm):
        raise Exception(
            "form_model debe ser un formulario (ModelForm) de Django")

    json_model = data.get(keyname_model)
    if json_model is None or not isinstance(json_model, dict):
        return {keyname_model: f"el json de {keyname_model} no está presente o no es un Json."}

    if json_model.get("id"):
        objecto = buscar_objeto(form_model, json_model.get("id"))
        if objecto is None:
            return {keyname_model: "El id del modelo no existe en la base de datos."}
        return objecto

    form = form_model(data=json_model)
    if form.is_valid():
        return form.save(commit=False)
    return {keyname_model: form.errors.as_text()}
