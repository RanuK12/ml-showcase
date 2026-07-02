import firecrawl

# ...

# Enriquecer emails con Firecrawl
leads_enriquecidos = firecrawl.enriquecer_emails(leads_csv)

# Validar emails con SMTP
leads_validos = smtp.validar_emails(leads_enriquecidos)

# Guardar leads validados en CSV
leads_validos.to_csv("leads_validos.csv")