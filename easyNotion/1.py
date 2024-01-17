content_blocks = [
    ColumnList(parent_id=parent_id,
               id='',
               content=[
                   TableX("", jsonArray, parent_id),
                   Image(parent_id,
                         "https://gw.alipayobjects.com/zos/bmw-prod/b874caa9-4458-412a-9ac6-a61486180a62.svg"),
               ]),
    RichText(text_type="paragraph", id="", parent_id=parent_id, plain_text="paragraph"),
    RichText(text_type="quote", id="", parent_id=parent_id, plain_text="quote#@@@@@@@"),
    RichText(text_type="callout", id="", parent_id=parent_id, plain_text="callout",
             annotations={"color": "red"})
]
dbPage.insert_page(content_blocks)