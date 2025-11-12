import pandas as pd
import io

def process_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=lambda x: x.strip())
    required = ['SKU','Planned_Qty','Received_Qty','EBO_Qty','D2C_Qty','LFR_Qty']
    for c in required:
        if c not in df.columns:
            df[c] = 0
    def calc(row):
        EBO = float(row['EBO_Qty'] or 0)
        D2C = float(row['D2C_Qty'] or 0)
        LFR = float(row['LFR_Qty'] or 0)
        Received = float(row['Received_Qty'] or 0)
        ignore_LFR = LFR < 10
        total = EBO + D2C if ignore_LFR else EBO + D2C + LFR
        ebo_pct = (EBO/total) if total else 0
        d2c_pct = (D2C/total) if total else 0
        lfr_pct = 0 if ignore_LFR else (LFR/total if total else 0)
        adj_received = Received - LFR if ignore_LFR else Received
        rec_ebo = round(adj_received * ebo_pct)
        rec_d2c = round(adj_received * d2c_pct)
        rec_lfr = 0 if ignore_LFR else round(adj_received * lfr_pct)
        return pd.Series({
            'EBO_%': round(ebo_pct*100,2),
            'D2C_%': round(d2c_pct*100,2),
            'LFR_%': round(lfr_pct*100,2),
            'Rec_EBO_Qty': int(rec_ebo),
            'Rec_D2C_Qty': int(rec_d2c),
            'Rec_LFR_Qty': int(rec_lfr),
            'Adj_Received_Qty': int(adj_received)
        })
    res = df.join(df.apply(calc, axis=1))
    return res

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Processed')
    output.seek(0)
    return output.read()
