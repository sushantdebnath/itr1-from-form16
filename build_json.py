import json
from models import ITRPayload
from datetime import date

def sanitize(obj):
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize(v) for v in obj]
    elif isinstance(obj, date):
        return obj.isoformat()
    elif hasattr(obj, "__dataclass_fields__"):
        return sanitize(vars(obj))
    else:
        return obj

def build_itr_json(taxpayer, ctx, f16, comp, input_pdf, out_json):
    payload_model = ITRPayload(
        ay=ctx.ay,
        taxpayer=taxpayer,
        context=ctx,
        income=f16.salary,
        deductions=f16.deductions,
        computed=comp,
        tds=f16.tds_list,
    )
    payload = sanitize(payload_model)  # Convert dataclasses to dict
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

