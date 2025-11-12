import pandas as pd, io
def process_input(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    for _, row in df.iterrows():
        section = str(row.get('section','MT')).upper()
        style = str(row.get('styleCode','OR45')).upper()
        colors = str(row.get('colorCodes','BLK,WHT')).replace(';',',').replace(':',',').split(',')
        sizes = str(row.get('sizeCodes','SML,MED')).replace(';',',').replace(':',',').split(',')
        def parse_list(s):
            s = str(s)
            for sep in [',',';',':']:
                if sep in s:
                    return [float(x) for x in s.split(sep) if x!='']
            return []
        eboRat = parse_list(row.get('eboRatios','1,1'))
        d2cQty = parse_list(row.get('d2cQuantities','10:10'))
        lfrRat = parse_list(row.get('lfrRatios','1,1'))
        eboTotal = float(row.get('eboTotal',100))
        lfrTotal = float(row.get('lfrTotal',80))
        n = len(sizes)
        if len(eboRat)!=n:
            eboRat = [1]*n
        if len(d2cQty)!=n:
            d2cQty = [0]*n
        if len(lfrRat)!=n:
            lfrRat = [1]*n
        eboSum = sum(eboRat)
        lfrSum = sum(lfrRat)
        ebo_per_size = [(r/eboSum)*eboTotal for r in eboRat]
        lfr_per_size = [(r/lfrSum)*lfrTotal for r in lfrRat]
        for color in colors:
            for i,size in enumerate(sizes):
                sku = f"{section}{style}{color}{size}"
                ebo_qty = round(ebo_per_size[i]/len(colors))
                d2c_qty = round(d2cQty[i]/len(colors)) if d2cQty else 0
                lfr_qty = round(lfr_per_size[i]/len(colors))
                out.append({'SKU':sku,'EBO':ebo_qty,'D2C':d2c_qty,'LFR':lfr_qty,'Total_Allocated_Qty':ebo_qty+d2c_qty+lfr_qty})
    return pd.DataFrame(out)

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    df.to_excel(buf, index=False, sheet_name='SKU_Allocations')
    buf.seek(0)
    return buf.read()
