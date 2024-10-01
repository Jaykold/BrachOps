def escape_xml(escape:str)-> str:
    return (
        escape
        .replace('<', '&lt;')
        .replace('>', '&gt;')
    )