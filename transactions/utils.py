

from django.forms import ModelForm
from django.db.models import Model
from typing import Union


def search_in_model(data: dict, field_names: list, model: Model, queryset=False) -> list:
    """La función busca un objeto en el modelo usando los campos y filtros dados y devuelve un array.

    La idea es que en el backend se especique los campos y los filtros permitidos para hacer la consulta en el modelo dado, y en el
    frontend se debe especificar los mismo nombres de campos.

    - data : es un json que viene del frontend y debe contener los mismo nombres de campos especificados en `field_names`
    - field_names : es una lista de nombres de campos que tiene la siguiente sintaxis: ["nombreDeCampo1__filtroDeDjango", "nombreDeCampo2"].
    Un ejempo más real seria: ["tipo_vehiculo", "placa__icontains"] indica que se filtrarán los resultados usando los campos 'tipo_vehiculo' y 'placa' y 
    el campo `placa` usa el filtro de consulta '__icontains' para no distinguir entre mayusculas y minuscula.

    """
    # Si uno de los valores de un campo esta vacio devuelve una lista vacia.
    for value in data.values():
        if value=="":
            return []

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
        result = model.objects.filter(**filter)
        if queryset==True:
            return result
        return list(result.values())
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


def checker(data: dict, form_model: ModelForm, keyname_model: str = None, new_object=True) -> Union[Model, dict]:
    """La función devuelve una instancia de la base de datos del modelo dado o una instancia nueva del modelo dado.
    
    - Si data tiene un campo `id` busca en la base de datos usando el modelo dado y si encuentra devuelve una instancia sino, devuelve un diccionario con el error.
    - Si data no contiene un campo `id` se da por hecho que los datos de data son para crear una instancia nueva usando el modelo dado. Si los
    datos son validos devuelve una instancia usando el modelo dado sino, devuelve un diccionario con el errores de validación.

    La función checker toma tres argumentos: 
    - data, 
    - form_model
    - ~keyname_model~.
    - new_object : True por defecto, pero si se establece en False la función no intentará crear una instancia usando del modelo en caso que no este en campo `id` en data.

    data: {
        "model_name":{"id":"1", "nombre"...}
    }
    """
    if issubclass(form_model, ModelForm) is False:
        raise Exception(
            "form_model debe ser un formulario (ModelForm) de Django")
            
    objecto = None
    if keyname_model is None:
        keyname_model = form_model.Meta.model.__name__.lower()

    json_model = data.get(keyname_model)
    if json_model is None or not isinstance(json_model, dict):
        return {keyname_model: f"el json de {keyname_model} no está presente o no es un Json."}

    if json_model.get("id"):
        objecto = buscar_objeto(form_model, json_model.get("id"))
        if objecto is None:
            return {keyname_model: "El id del modelo no existe en la base de datos."}
        return objecto

    if new_object is False:
        return {keyname_model: "No hay un campo `id` para consultar en la db."}

    form = form_model(data=json_model)
    if form.is_valid():
        return form.save(commit=False)
    return {keyname_model: form.errors.as_text()}
