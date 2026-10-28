"""Reproduce the quantified cash schedules from supplied CSV records; USD millions."""
from pathlib import Path
import csv
from decimal import Decimal as D
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
def read(name):
    with (ROOT/'records/Cash_Operations'/name).open() as f:return list(csv.DictReader(f))
def write(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
entities=['INC','EUR','BEL']; floors={'INC':D(40),'EUR':D(8),'BEL':D(6)}
opening=read('opening_bank_control.csv'); postings=read('bank_posting_batches.csv')
bal={e:sum((D(r['cash_USDm']) for r in opening if r['entity']==e and r['account']=='operating'),D(0)) for e in entities}
ledger=[]
for i,r in sorted(enumerate(postings,2),key=lambda x:(x[1]['value_date'],x[0])):
    e=r['entity'];bal[e]+=D(r['signed_cash_USDm'])
    ledger.append(dict(source_file='bank_posting_batches.csv',source_line=i,**r,running_entity_cash_USDm=bal[e]))
write('01_posted_ledger.csv',ledger)
recon=[]
for e in entities:
    start=next(D(r['cash_USDm']) for r in opening if r['entity']==e and r['account']=='operating')
    ps=[r for r in postings if r['entity']==e]
    receipts=sum((D(r['signed_cash_USDm']) for r in ps if r['description']=='customer cash batches'),D(0))
    operating=sum((D(r['signed_cash_USDm']) for r in ps if r['description']=='payroll supplier tax and capex batches'),D(0))
    other=sum((D(r['signed_cash_USDm']) for r in ps if r['description'] not in ['customer cash batches','payroll supplier tax and capex batches']),D(0))
    assert start+receipts+operating+other==bal[e]
    recon.append(dict(entity=e,opening_20240627_USDm=start,customer_receipts_USDm=receipts,ordinary_payments_signed_USDm=operating,other_posted_net_USDm=other,closing_20240802_USDm=bal[e],operating_floor_USDm=floors[e],headroom_USDm=bal[e]-floors[e]))
write('02_bank_rollforward.csv',recon)
assert sum(bal.values())==D(188)
diary=read('weekly_diary_issued_20240726.csv'); rows=[]
for scenario,draw,pay in [('queued_payment_no_new_funding',D(0),True),('conditional_full_remaining_bridge',D(150),True),('ordinary_batches_only_payment_unresolved',D(0),False)]:
    cash=bal.copy()
    for r in diary:
        e=r['entity'];week=r['week_ending'];start=cash[e]
        receipt=D(r['customer_receipts_USDm']);disb=D(r['operating_disbursements_USDm'])
        bridge=draw if week=='2024-08-16' and e=='INC' else D(0)
        boeing=D('150.6') if pay and week=='2024-08-16' and e=='INC' else D(0)
        cash[e]=start+receipt-disb+bridge-boeing
        rows.append(dict(scenario=scenario,week_ending=week,entity=e,opening_USDm=start,customer_receipts_USDm=receipt,ordinary_disbursements_USDm=disb,boeing_20240814_outflow_USDm=boeing,proposed_bridge_inflow_USDm=bridge,closing_quantified_cash_USDm=cash[e],floor_USDm=floors[e],headroom_USDm=cash[e]-floors[e],incremental_funding_to_floor_USDm=max(D(0),floors[e]-cash[e]),basis='Quantified items only; interest and fees unresolved; proposed funding not authorised'))
write('03_august_cash_diary.csv',rows)
summary=[]
for scenario in dict.fromkeys(r['scenario'] for r in rows):
    for week in sorted({r['week_ending'] for r in rows}):
        rs=[r for r in rows if r['scenario']==scenario and r['week_ending']==week]
        summary.append(dict(scenario=scenario,week_ending=week,group_closing_USDm=sum(r['closing_quantified_cash_USDm'] for r in rs),group_floor_USDm=D(54),entity_specific_funding_need_USDm=sum(r['incremental_funding_to_floor_USDm'] for r in rs),group_headroom_USDm=sum(r['headroom_USDm'] for r in rs)))
write('04_diary_totals.csv',summary)
assert next(r for r in rows if r['scenario']=='queued_payment_no_new_funding' and r['week_ending']=='2024-08-30' and r['entity']=='INC')['closing_quantified_cash_USDm']==D('-98.6')
print('Built four schedules. Opening operating cash 206.0; closing operating cash 188.0; restricted cash separately 28.1.')
