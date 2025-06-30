from viur.core import conf
from viur.core.prototypes import List, Tree
import os, json, anthropic


def query_anthropic(
        user_prompt: str, 
        model:str="claude-3-7-sonnet-20250219", # Name of the model to use
        max_tokens:int=1024, 
        temperature:float=1.0,
        modules_to_include:list[str]=None,
        enable_caching:bool=False,
        max_thinking_tokens:int=0,  # disables thinking if <= 0
        system_prompt:str="You are a coding-assistant that helps develop python-code for accessing a viur-backend. You only output json-strings containing a single key named \"code\".",
        dry_run:bool=False,
        anthropic_api_key:str=None
):
    with open(os.path.join(conf.instance.project_base_path,"ai","contexts","scriptor_docs.txt"), "r") as scriptor_docs_file:
        scriptor_docs_txt_data = scriptor_docs_file.read()

    llm_params = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": [{
            "type": "text",
            "text": system_prompt
        }],
        "messages": [{
            "role": "user",
            "content": []
        }]
    }

    # add docs to system prompt (with or without caching)
    scriptor_doc_system_param = {
        "type": "text",
        "text": scriptor_docs_txt_data,
    }
    if enable_caching:
        scriptor_doc_system_param["cache_control"] = {"type": "ephemeral"}
    llm_params["system"].append(scriptor_doc_system_param)

    # thinking configuration
    if max_thinking_tokens > 0:
        llm_params["thinking"] = {
            "type": "enabled",
            "budget_tokens": max_thinking_tokens
        }

    # add module structures
    if modules_to_include is not None:
        structures_from_viur = {}
        for module_name in modules_to_include:
            module = getattr(conf.main_app.vi, module_name, None)
            if not module:
                continue

            if isinstance(module,List):
                if module_name not in structures_from_viur:
                    structures_from_viur[module_name] = module.structure()
            elif  isinstance(module,Tree):
                if module_name not in structures_from_viur:
                    structures_from_viur[module_name] = {
                        "node": module.structure(skelType="node"),
                        "leaf": module.structure(skelType="leaf")
                    }
            else:
                raise ValueError(f"""The module should should be a instance of "tree" or "list". "{module}" is unsupported.""")
            
        selected_module_structures = {"module_structures": structures_from_viur}
        selected_module_structures_description = json.dumps(selected_module_structures, indent=2)

        if selected_module_structures["module_structures"]:
            llm_params["messages"][0]["content"].append({
                "type": "text",
                "text": selected_module_structures_description
            })

    # finally append user prompt
    llm_params["messages"][0]["content"].append({
        "type": "text",
        "text": user_prompt
    })

    if dry_run:
        return llm_params, None
    else:
        anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        message = anthropic_client.messages.create(**llm_params)
        return llm_params, message