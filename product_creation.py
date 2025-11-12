import pandas as pd, io, re
def process_sheets(sheet1: pd.DataFrame, sheet2: pd.DataFrame, keywords: str, styleid: str) -> pd.DataFrame:
    s1 = sheet1.copy(); s2 = sheet2.copy()
    s1.columns = [str(c).strip() for c in s1.columns]
    s2.columns = [str(c).strip() for c in s2.columns]
    key_col=None
    for candidate in ['Internal Reference','Internal_Reference','internal reference','SKU','sku','InternalRef']:
        for c in s1.columns:
            if candidate.lower() in c.lower():
                key_col=c; break
        if key_col: break
    mrp_col=None
    for candidate in ['Sales Price','Sales\xa0Price','mrp','MRP','Price']:
        for c in s1.columns:
            if candidate.lower() in c.lower():
                mrp_col=c; break
        if mrp_col: break
    barcode_col=None
    for candidate in ['Barcode','barcode','EAN']:
        for c in s1.columns:
            if candidate.lower() in c.lower():
                barcode_col=c; break
        if barcode_col: break
    desc_col=None
    for candidate in ['Sku Desc','sku desc','sku description','description']:
        for c in s2.columns:
            if candidate.lower() in c.lower():
                desc_col=c; break
        if desc_col: break
    keys = [k.strip().lower() for k in re.split('[,;:]+', keywords) if k.strip()]
    out=[]
    for _, r in s1.iterrows():
        sku = str(r.get(key_col,'')).strip()
        if not sku: continue
        sub = sku[6:9] if len(sku)>=9 else sku[-6:-3] if len(sku)>=6 else sku
        if not any(k in sub.lower() for k in keys):
            continue
        mrp = r.get(mrp_col,'')
        barcode = r.get(barcode_col,'')
        desc = ''
        if desc_col:
            matched = s2[s2.apply(lambda x: str(x).lower().find(str(styleid).lower())!=-1, axis=1)]
            if not matched.empty:
                desc = str(matched.iloc[0].get(desc_col,''))
        color = sub.upper() if isinstance(sub,str) else ''
        size = sku[-3:]
        out.append({
            'clientSkuId': sku,
            'brandId': 'TECHNOSPORT',
            'category': 'NA',
            'color': color,
            'hsnId': '',
            'imageUrl': '',
            'mrp': mrp,
            'name': desc,
            'size': size,
            'styleId': styleid,
            'taxRule': 'GST_APPAREL',
            'isBundled': 'FALSE',
            'isSerialCodeRequired': 'FALSE',
            'barcode': barcode,
            'Section': desc.split(' ')[1] if isinstance(desc,str) and len(desc.split(' '))>1 else 'NA',
            'Fit type': 'NA',
            'season': 'YEAR ROUND',
            'Color name': color,
            'Neck Type': 'NA',
            'Pattern': 'NA',
            'subcategory': 'NA',
            'Fabric': 'NA',
            'Sleeve Type': 'NA',
            'segment': 'NA',
            'Technology': 'TECHNOSPORT',
            'style_code': sku[2:9] if len(sku)>9 else styleid,
            'master_category': 'APPAREL'
        })
    return pd.DataFrame(out)

def to_csv_bytes(df: pd.DataFrame) -> bytes:
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode('utf-8')
