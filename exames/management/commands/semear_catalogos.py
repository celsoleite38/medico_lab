"""
Comando para semear catálogos e base de conhecimento do sistema.

Uso: python manage.py semear_catalogos [--reset]

Popula: exames, medicamentos, valores de referência, modelos de atestado,
         e base de conhecimento do motor de sugestões.
"""
from django.core.management.base import BaseCommand

# Exames laboratoriais/imagem comuns no Brasil (TUSS-like codes omitted for simplicity)
CATALOGO_EXAMES = [
    # Hematologia
    ("Hemograma completo", "laboratorial", "Jejum de 8h"),
    ("Hemoglobina", "laboratorial", ""),
    ("Hematócrito", "laboratorial", ""),
    ("Leucograma", "laboratorial", ""),
    ("Plaquetas", "laboratorial", ""),
    ("VHS", "laboratorial", ""),
    ("PCR quantitativa", "laboratorial", ""),
    ("Reticulócitos", "laboratorial", ""),
    ("Ferro sérico", "laboratorial", "Jejum de 8h"),
    ("Ferritina", "laboratorial", "Jejum de 8h"),
    ("Transferrina", "laboratorial", "Jejum de 8h"),
    ("Transferrina saturada", "laboratorial", ""),
    ("Hb eletroforese", "laboratorial", ""),
    ("Teste do pezinho", "laboratorial", ""),
    ("Coagulograma", "laboratorial", ""),
    ("TP", "laboratorial", ""),
    ("TTPa", "laboratorial", ""),
    ("INR", "laboratorial", ""),
    ("Fator V de Leiden", "laboratorial", ""),
    ("Proteína C", "laboratorial", ""),
    ("Proteína S", "laboratorial", ""),
    ("Antitrombina III", "laboratorial", ""),

    # Bioquímica
    ("Glicemia de jejum", "laboratorial", "Jejum de 8h"),
    ("HbA1c (Hemoglobina glicada)", "laboratorial", ""),
    ("HOMA-IR", "laboratorial", "Jejum de 8h"),
    ("Curva glicêmica", "laboratorial", "Jejum de 8h"),
    ("Ureia", "laboratorial", ""),
    ("Creatinina", "laboratorial", ""),
    ("Clearance de creatinina", "laboratorial", ""),
    ("Ácido úrico", "laboratorial", ""),
    ("Colesterol total", "laboratorial", "Jejum de 12h"),
    ("HDL", "laboratorial", "Jejum de 12h"),
    ("LDL", "laboratorial", "Jejum de 12h"),
    ("Triglicerídeos", "laboratorial", "Jejum de 12h"),
    ("VLDL", "laboratorial", "Jejum de 12h"),
    ("Proteína C reativa", "laboratorial", ""),
    ("TGO (AST)", "laboratorial", ""),
    ("TGP (ALT)", "laboratorial", ""),
    ("Gama GT", "laboratorial", ""),
    ("Fosfatase alcalina", "laboratorial", ""),
    ("Bilirrubina total", "laboratorial", ""),
    ("Bilirrubina direta", "laboratorial", ""),
    ("Bilirrubina indireta", "laboratorial", ""),
    ("Amilase", "laboratorial", ""),
    ("Lipase", "laboratorial", ""),
    ("LDH", "laboratorial", ""),
    ("CK (Creatinoquinase)", "laboratorial", ""),
    ("CK-MB", "laboratorial", ""),
    ("Troponina", "laboratorial", ""),
    ("BNP / ProBNP", "laboratorial", ""),
    ("Lactato", "laboratorial", ""),

    # Elétrolitos e gases
    ("Sódio", "laboratorial", ""),
    ("Potássio", "laboratorial", ""),
    ("Cálcio", "laboratorial", ""),
    ("Cálio sérico", "laboratorial", ""),
    ("Fósforo", "laboratorial", ""),
    ("Magnésio", "laboratorial", ""),
    ("Cloreto", "laboratorial", ""),
    ("Gasometria arterial", "laboratorial", ""),
    ("Gasometria venosa", "laboratorial", ""),

    # Hormônios
    ("TSH", "laboratorial", ""),
    ("T4 livre", "laboratorial", ""),
    ("T4 total", "laboratorial", ""),
    ("T3", "laboratorial", ""),
    ("Anti-TPO", "laboratorial", ""),
    ("Anti-Tireoglobulina", "laboratorial", ""),
    ("Cortisol", "laboratorial", ""),
    ("PTH (Paratormônio)", "laboratorial", ""),
    ("Insulina", "laboratorial", "Jejum de 8h"),
    ("Testosterona total", "laboratorial", ""),
    ("Testosterona livre", "laboratorial", ""),
    ("Estradiol", "laboratorial", ""),
    ("Progesterona", "laboratorial", ""),
    ("FSH", "laboratorial", ""),
    ("LH", "laboratorial", ""),
    ("Prolactina", "laboratorial", ""),
    ("DHEA-S", "laboratorial", ""),
    ("Vitamina D", "laboratorial", ""),
    ("Vitamina B12", "laboratorial", ""),
    ("Ácido fólico", "laboratorial", ""),
    ("Homocisteína", "laboratorial", ""),

    # Imunologia / Sorologias
    ("VDRL", "laboratorial", ""),
    ("Anti-HIV", "laboratorial", ""),
    ("Hepatite B (HBsAg)", "laboratorial", ""),
    ("Anti-HBc", "laboratorial", ""),
    ("Anti-HBs", "laboratorial", ""),
    ("Anti-HCV", "laboratorial", ""),
    ("Fator reumatóide", "laboratorial", ""),
    ("ANA (Anticorpo antinuclear)", "laboratorial", ""),
    ("Anti-DNA", "laboratorial", ""),
    ("Complemento C3", "laboratorial", ""),
    ("Complemento C4", "laboratorial", ""),
    ("IgA", "laboratorial", ""),
    ("IgG", "laboratorial", ""),
    ("IgM", "laboratorial", ""),
    ("IgE total", "laboratorial", ""),
    ("D-dímero", "laboratorial", ""),
    ("Troponina I", "laboratorial", ""),
    ("Troponina T", "laboratorial", ""),
    ("Procalcitonina", "laboratorial", ""),

    # Urinálise
    ("Urinálise", "laboratorial", ""),
    ("Urocultura", "laboratorial", ""),
    ("Microalbuminúria", "laboratorial", "Coleta de urina 24h"),
    ("Clearance de creatinina urinário", "laboratorial", "Coleta de urina 24h"),
    ("Cristais na urina", "laboratorial", ""),
    ("Proteína C reativa urinária", "laboratorial", ""),

    # Fezes
    ("Ecoparasitológico", "laboratorial", ""),
    ("Sangue oculto nas fezes", "laboratorial", ""),
    ("Coproscopia", "laboratorial", ""),
    ("Pesquisa de helmintos", "laboratorial", ""),
    ("Calprotectina fecal", "laboratorial", ""),
    ("Toxina de Clostridium difficile", "laboratorial", ""),

    # Imagem
    ("Raio-X de tórax", "imagem", ""),
    ("Raio-X de abdomen", "imagem", ""),
    ("Raio-X de crânio", "imagem", ""),
    ("Raio-X de coluna", "imagem", ""),
    ("Raio-X de membro superior", "imagem", ""),
    ("Raio-X de membro inferior", "imagem", ""),
    ("Ultrassonografia abdominal", "imagem", "Jejum de 6h"),
    ("Ultrassonografia pélvica", "imagem", "Bexiga cheia"),
    ("Ultrassonografia de tireóide", "imagem", ""),
    ("Ultrassonografia de mama", "imagem", ""),
    ("Ultrassonografia de quadril", "imagem", ""),
    ("Ultrassonografia obstétrica", "imagem", ""),
    ("Ultrassonografia com Doppler", "imagem", ""),
    ("Ultrassonografia transvaginal", "imagem", ""),
    ("Eletrocardiograma (ECG)", "procedimento", ""),
    ("Eletroencefalograma (EEG)", "procedimento", ""),
    ("Ecocardiograma", "procedimento", ""),
    ("Ecocardiograma fetal", "procedimento", ""),
    ("Teste ergométrico", "procedimento", "Evitar refeição 2h antes"),
    ("Teste de esforço", "procedimento", ""),
    ("Holter 24h", "procedimento", ""),
    ("MAPA 24h", "procedimento", ""),
    ("Pletismografia", "procedimento", ""),
    ("Densitometria óssea", "procedimento", ""),
    ("Tomografia computadorizada", "imagem", ""),
    ("Ressonância magnética", "imagem", ""),
    ("Mamografia", "imagem", ""),
    ("Densitometria", "imagem", ""),
    ("Angiotomografia", "imagem", ""),
    ("Punção lombar", "procedimento", ""),
    ("Biópsia", "procedimento", ""),
    ("Endoscopia digestiva alta", "procedimento", "Jejum de 8h"),
    ("Colonoscopia", "procedimento", "Preparo intestinal"),
    ("Broncoscopia", "procedimento", "Jejum de 6h"),
    ("Laringoscopia", "procedimento", ""),
    ("Audiometria", "procedimento", ""),
    ("Espirometria", "procedimento", ""),
    ("Cardiotocografia (CTG)", "procedimento", ""),
    ("Electromiografia (EMG)", "procedimento", ""),
    ("Velocidade de condução nervosa", "procedimento", ""),
    ("Biópsia de pele", "procedimento", ""),
    ("Cultura de secreção", "laboratorial", ""),
    ("Cultura de urina", "laboratorial", ""),
    ("Cultura de sangue (hemocultura)", "laboratorial", ""),
    ("Antibiograma", "laboratorial", ""),
    ("Pesquisa de BAAR", "laboratorial", ""),
    ("Teste tuberculínico (PPD)", "procedimento", ""),
    ("Teste do suor (fibrose cística)", "procedimento", ""),
    ("Teste ergométrico supervisionado", "procedimento", ""),
    ("Mamografia digital", "imagem", ""),
    ("Tomografia de tórax", "imagem", ""),
    ("Ressonância de crânio", "imagem", ""),
    ("Ressonância de coluna", "imagem", ""),
    ("Ressonância de joelho", "imagem", ""),
    ("Doppler carotídeo", "imagem", ""),
    ("Doppler venoso de membros inferiores", "imagem", ""),
    ("Raios-X de seios da face", "imagem", ""),
    ("Raios-X de articulação", "imagem", ""),
]

CATALOGO_MEDICAMENTOS = [
    # Analgésicos / Anti-inflamatórios
    ("Dipirona", "Dipirona", "500mg comp, 1g comp, 500mg gotas, 1g inj"),
    ("Paracetamol", "Paracetamol", "200mg comp, 500mg comp, 750mg comp, 200mg gotas"),
    ("Ibuprofeno", "Ibuprofeno", "400mg comp, 600mg comp"),
    ("Naproxeno", "Naproxeno", "250mg comp, 500mg comp"),
    ("Diclofenaco", "Diclofenaco", "50mg comp, 75mg gotas, 100mg supositório"),
    ("Nimesulida", "Nimesulida", "100mg comp, 100mg suspensão"),
    ("Meloxicam", "Meloxicam", "7.5mg comp, 15mg comp"),
    ("Indometacina", "Indometacina", "25mg comp, 50mg comp"),
    ("Ketoprofeno", "Ketoprofeno", "50mg comp, 100mg comp, 100mg inj"),
    ("Tramadol", "Cloridrato de Tramadol", "50mg comp, 100mg comp"),
    ("Codeína", "Fosfato de Codeína", "30mg comp"),
    ("Morfina", "Sulfato de Morfina", "10mg comp, 10mg/mL inj"),
    ("Cetorolaco", "Cetorolaco de trometamina", "30mg/mL inj, 10mg comp"),

    # Antibióticos
    ("Amoxicilina", "Amoxicilina", "500mg comp, 1g comp, 250mg suspensão"),
    ("Amoxicilina + Clavulanato", "Amoxicilina + Ácido Clavulânico", "625mg comp, 1g comp, 400mg suspensão"),
    ("Azitromicina", "Azitromicina", "500mg comp, 250mg comp, 200mg suspensão"),
    ("Ciprofloxacino", "Cloridrato de Ciprofloxacino", "500mg comp"),
    ("Levofloxacino", "Levofloxacino", "500mg comp"),
    ("Metronidazol", "Metronidazol", "250mg comp, 500mg comp"),
    ("Cefalexina", "Cefalexina", "500mg comp, 500mg suspensão"),
    ("Ceftriaxona", "Ceftriaxona", "1g inj, 2g inj"),
    ("Cefuroxima", "Cefuroxima", "250mg comp, 500mg comp"),
    ("Doxiciclina", "Cloridrato de Doxiciclina", "100mg comp"),
    ("Eritromicina", "Eritromicina", "500mg comp"),
    ("Clindamicina", "Clindamicina", "300mg comp, 600mg comp"),
    ("Sulfametoxazol + Trimetoprima", "SMT + TMP", "480mg comp, 960mg comp, gotas"),
    ("Nitrofurantoína", "Nitrofurantoína", "100mg comp"),
    ("Fluconazol", "Fluconazol", "150mg comp, 200mg comp"),

    # Anti-hipertensivos
    ("Losartana", "Potássio de Losartana", "50mg comp, 100mg comp"),
    ("Enalapril", "Maleato de Enalapril", "10mg comp, 20mg comp"),
    ("Captopril", "Captopril", "25mg comp"),
    ("Anlodipino", "Besilato de Anlodipino", "5mg comp, 10mg comp"),
    ("Hidroclorotiazida", "Hidroclorotiazida", "25mg comp"),
    ("Atenolol", "Cloridrato de Atenolol", "25mg comp, 50mg comp, 100mg comp"),
    ("Metoprolol", "Tartrato de Metoprolol", "50mg comp, 100mg comp"),
    ("Propranolol", "Cloridrato de Propranolol", "40mg comp, 80mg comp"),
    ("Bisoprolol", "Fumarato de Bisoprolol", "5mg comp, 10mg comp"),
    ("Valsartana", "Valsartana", "80mg comp, 160mg comp"),
    ("Irbesartana", "Irbesartana", "150mg comp, 300mg comp"),
    ("Candesartana", "Cilsexil de Candesartana", "8mg comp, 16mg comp"),
    ("Telmisartana", "Telmisartana", "40mg comp, 80mg comp"),
    ("Espironolactona", "Espironolactona", "25mg comp, 50mg comp"),
    ("Furosemida", "Furosemida", "40mg comp, 40mg/mL inj"),
    ("Hidroclorotiazida + Losartana", "HCTZ + Losartana", "50/12.5mg comp"),
    ("Enalapril + Hidroclorotiazida", "Enalapril + HCTZ", "10/25mg comp"),

    # Antidiabéticos
    ("Metformina", "Cloridrato de Metformina", "500mg comp, 850mg comp, 1000mg comp"),
    ("Gliclazida", "Gliclazida", "30mg comp MR, 80mg comp"),
    ("Glibenclamida", "Glibenclamida", "5mg comp"),
    ("Gliclazida + Metformina", "Gliclazida + Metformina", "30/500mg comp"),
    ("Insulina NPH", "Insulina Humana NPH", "100UI/mL frasco"),
    ("Insulina Regular", "Insulina Humana Regular", "100UI/mL frasco"),
    ("Insulina Glargina", "Insulina Glargina", "100UI/mL caneta"),
    ("Sitagliptina", "Fosfato de Sitagliptina", "50mg comp, 100mg comp"),
    ("Empagliflozina", "Diprogliflozina de Empagliflozina", "10mg comp, 25mg comp"),
    ("Dapagliflozina", "Propanodiol de Dapagliflozina", "5mg comp, 10mg comp"),
    ("Saxagliptina", "Cloridrato de Saxagliptina", "5mg comp"),
    ("Liraglutida", "Liraglutida", "6mg/mL caneta"),
    ("Semaglutida", "Semaglutida", "0.25/0.5mg caneta, 1mg caneta"),

    # Estatinas / Dislipidemia
    ("Sinvastatina", "Sinvastatina", "10mg comp, 20mg comp, 40mg comp"),
    ("Atorvastatina", "Cálcica de Atorvastatina", "10mg comp, 20mg comp, 40mg comp"),
    ("Rosuvastatina", "Cálcica de Rosuvastatina", "5mg comp, 10mg comp, 20mg comp"),
    ("Ezetimiba", "Ezetimiba", "10mg comp"),
    ("Fenofibrato", "Fenofibrato", "145mg comp, 200mg comp"),

    # Gastro
    ("Omeprazol", "Cápsulas de Omeprazol", "20mg cáps, 40mg cáps"),
    ("Pantoprazol", "Pantoprazol", "20mg comp, 40mg comp"),
    ("Esomeprazol", "Esomeprazol", "20mg comp, 40mg comp"),
    ("Ranitidina", "Cloridrato de Ranitidina", "150mg comp, 300mg comp"),
    ("Dramamina", "Dimenidrinato", "50mg comp"),
    ("Domperidona", "Maleato de Domperidona", "10mg comp, 10mg/mL gotas"),
    ("Metoclopramida", "Cloridrato de Metoclopramida", "10mg comp, 10mg/mL inj"),
    ("Creon", "Pancreatina (Pанкреатина)", "10.000 UI cáps"),
    ("Buscopan", "Escopolamina N-brometo", "10mg comp"),
    ("Neosaldina", "Dipirona + Citrato de Fenazopiridina", "comp"),

    # Respiratórios
    ("Salbutamol", "Sulfato de Salbutamol", "100mcg aerossol, 2mg comp, 4mg comp, gotas"),
    ("Budesonida", "Budesonida", "200mcg aerossol, 400mcg aerossol"),
    ("Beclometasona", "Dipropionato de Beclometasona", "250mcg aerossol"),
    ("Fluticasona", "Propionato de Fluticasona", "50mcg nasal, 250mcg aerossol"),
    ("Montelucaste", "Sódico de Montelucaste", "4mg comp, 5mg comp, 10mg comp"),
    ("Desloratadina", "Desloratadina", "5mg comp"),
    ("Loratadina", "Loratadina", "10mg comp"),
    ("Cetirizina", "Dicloridrato de Cetirizina", "10mg comp, 10mg/mL gotas"),
    ("Ambroxol", "Cloridrato de Ambroxol", "30mg comp, 75mg comp, gotas"),
    ("Acetilcisteína", "Acetilcisteína", "600mg comp, 200mg comp"),
    ("Fenilefrina", "Cloridrato de Fenilefrina", "10mg comp"),
    ("Pseudoefedrina", "Cloridrato de Pseudoefedrina", "60mg comp"),

    # Cardiovasculares
    ("AAS (Ácido Acetilsalicílico)", "Ácido Acetilsalicílico", "100mg comp, 500mg comp"),
    ("Clopidogrel", "Bissulfato de Clopidogrel", "75mg comp"),
    ("Varfarina", "Varfarena Sódica", "2.5mg comp, 5mg comp"),
    ("Rivaroxabana", "Rivaroxabana", "10mg comp, 15mg comp, 20mg comp"),
    ("Digoxina", "Digoxina", "0.25mg comp"),
    ("Amiodarona", "Cloridrato de Amiodarona", "200mg comp"),
    ("Hidrocloroquina", "Sulfato de Hidrocloroquina", "250mg comp"),

    # Hormônios / Endócrino
    ("Levotiroxina", "Levotiroxina Sódica", "25mcg, 50mcg, 75mcg, 100mcg comp"),
    ("Prednisona", "Prednisona", "5mg comp, 20mg comp, 50mg comp"),
    ("Dexametasona", "Fosfato Dissódico de Dexametasona", "4mg comp, 4mg/mL inj"),
    ("Metilprednisolona", "Succinato Sódico de Metilprednisolona", "4mg comp, 125mg inj, 500mg inj"),
    ("Acetato de Ciproterona", "Acetato de Ciproterona", "50mg comp"),
    ("Estradiol", "Valerato de Estradiol", "1mg comp, 0.5mg comp, gel"),
    ("Progesterona", "Progesterona micronizada", "100mg cáps, 200mg cáps"),
    ("Acetato de Medroxiprogesterona", "Acetato de Medroxiprogesterona", "2.5mg comp, 5mg comp, 150mg/mL inj"),

    # Neurológicos / Psiquiátricos
    ("Diazepam", "Diazepam", "5mg comp, 10mg comp"),
    ("Rivotril", "Clonazepam", "0.5mg comp, 2mg comp"),
    ("Alprazolam", "Alprazolam", "0.25mg comp, 0.5mg comp"),
    ("Sertralina", "Cloridrato de Sertralina", "50mg comp, 100mg comp"),
    ("Fluoxetina", "Cloridrato de Fluoxetina", "20mg comp"),
    ("Escitalopram", "Oxalato de Escitalopram", "10mg comp, 20mg comp"),
    ("Amitriptilina", "Cloridrato de Amitriptilina", "25mg comp, 50mg comp"),
    ("Duloxetina", "Cloridrato de Duloxetina", "30mg comp, 60mg comp"),
    ("Venlafaxina", "Cloridrato de Venlafaxina", "75mg comp, 150mg comp"),
    ("Quetiapina", "Fumarato de Quetiapina", "25mg comp, 50mg comp, 100mg comp"),
    ("Olanzapina", "Olanzapina", "5mg comp, 10mg comp"),
    ("Risperidona", "Risperidona", "1mg comp, 2mg comp"),
    ("Bupropiona", "Cloridrato de Bupropiona", "150mg comp, 300mg comp"),
    ("Carbamazepina", "Carbamazepina", "200mg comp"),
    ("Valproato", "Ácido Valproico / Valproato de Sódio", "250mg comp, 500mg comp"),
    ("Fenitoína", "Fenitoína Sódica", "100mg comp"),
    ("Topiramato", "Topiramato", "25mg comp, 50mg comp, 100mg comp"),
    ("Levetiracetam", "Levetiracetam", "500mg comp, 1000mg comp"),
    ("Gabapentina", "Gabapentina", "300mg comp, 600mg comp"),
    ("Pregabalina", "Pregabalina", "75mg comp, 150mg comp"),

    # Dermatológicos
    ("Hidrocortisona", "Acetato de Hidrocortisona", "1% pomada, 0.5% pomada"),
    ("Betametasona", "Dipropionato de Betametasona", "0.05% pomada, 0.05% loção"),
    ("Miconazol", "Nitrato de Miconazol", "2% creme"),
    ("Clotrimazol", "Clotrimazol", "1% creme"),
    ("Permetrina", "Permetrina", "5% loção"),
    ("Ivermectina", "Ivermectina", "6mg comp"),
    ("Mupirocina", "Mupirocina", "2% pomada"),
    ("Fusidato de Sódio", "Fusidato de Sódio", "2% pomada"),

    # Vitaminas / Suplementos
    ("Vitamina D3", "Colecalciferol", "7.000UI comp, 50.000UI cáps"),
    ("Vitamina B12", "Cianocobalamina", "5.000mcg comp, 5.000mcg inj"),
    ("Ferro (sulfato ferroso)", "Sulfato Ferroso", "40mg comp, 200mg comp"),
    ("Ácido fólico", "Ácido Fólico", "5mg comp"),
    ("Calcio + Vitamina D", "Carbonato de Cálcio + Colecalciferol", "600+400 comp"),
    ("Centrum", "Multivitamínico", "comp"),
    ("Supradyn", "Multivitamínico", "comp, efervescente"),

    # Outros comuns
    ("Dipirona + Orfenadrina", "Dipirona + Cloridrato de Orfenadrina", "comp"),
    ("Piroxicam", "Piroxicam", "20mg comp, 20mg gel"),
    ("Celecoxibe", "Celecoxibe", "200mg comp"),
    ("Colchicina", "Colchicina", "0.5mg comp"),
    ("Alopurinol", "Alopurinol", "100mg comp, 300mg comp"),
    ("Febuxostat", "Febuxostat", "80mg comp"),
]

# Valores de referência: (exame nome, analito, regex, unidade, min, max, orientacao_alto, orientacao_baixo)
VALORES_REFERENCIA = [
    ("Hemograma completo", "Hemoglobina", r'Hemoglobina\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'g/dL', 12.0, 16.0,
     "Pode indicar policitemia, desidratação ou doença pulmonar", "Pode indicar anemia"),
    ("Hemograma completo", "Hematócrito", r'Hemat[oó]crito\s*[:=]?\s*([0-9]+[.,][0-9]+)', '%', 36.0, 48.0,
     "Pode indicar policitemia", "Pode indicar anemia ou hemorragia"),
    ("Hemograma completo", "Plaquetas", r'Plaquetas\s*[:=]?\s*([0-9]+)', 'x10³/µL', 150.0, 450.0,
     "Risco de trombose", "Risco de sangramento"),
    ("Hemograma completo", "Leucócitos", r'Leuc[oó]citos\s*[:=]?\s*([0-9]+)', 'x10³/µL', 4.0, 11.0,
     "Pode indicar infecção, leucocitose", "Pode indicar infecção grave, imunossupressão"),
    ("Glicemia de jejum", "Glicemia", r'[Gg]licemia\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mg/dL', 70.0, 100.0,
     "Pré-diabetes (100-125) ou diabetes (>=126)", "Hipoglicemia"),
    ("HbA1c (Hemoglobina glicada)", "HbA1c", r'HbA1[cC]\s*[:=]?\s*([0-9]+[.,][0-9]+)', '%', 4.0, 5.7,
     "Pré-diabetes (5.7-6.4) ou diabetes (>=6.5)", ""),
    ("Creatinina", "Creatinina", r'[Cc]reatinina\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mg/dL', 0.6, 1.2,
     "Disfunção renal", ""),
    ("Ureia", "Ureia", r'[Uu]reia\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mg/dL', 10.0, 50.0,
     "Disfunção renal, desidratação, catabolismo aumentado", ""),
    ("Ácido úrico", "Ácido úrico", r'[Aá]cido\s+[Uu]rico\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mg/dL', 3.5, 7.2,
     "Hiperuricemia, gota, síndrome metabólica", ""),
    ("Colesterol total", "Colesterol total", r'[Cc]olesterol\s+[Tt]otal\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mg/dL', 0, 200.0,
     "Risco cardiovascular aumentado", ""),
    ("HDL", "HDL", r'HDL\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mg/dL', 40.0, 999.0,
     "", "Risco cardiovascular aumentado, colesterol bom baixo"),
    ("LDL", "LDL", r'LDL\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mg/dL', 0, 130.0,
     "Risco cardiovascular aumentado", ""),
    ("Triglicerídeos", "Triglicerídeos", r'[Tt]riglicer[ií]deos\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mg/dL', 0, 150.0,
     "Hipertrigliceridemia, risco pancreatite", ""),
    ("TGO (AST)", "TGO", r'(?:TGO|AST)\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'U/L', 5.0, 40.0,
     "Lesão hepática, miocardite, dano muscular", ""),
    ("TGP (ALT)", "TGP", r'(?:TGP|ALT)\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'U/L', 7.0, 56.0,
     "Lesão hepática (mais específico que TGO)", ""),
    ("Sódio", "Sódio", r'[Ss]ódio\s*[:=]?\s*([0-9]+)', 'mEq/L', 136.0, 145.0,
     "Hipernatremia, desidratação", "Hiponatremia"),
    ("Potássio", "Potássio", r'[Pp]ot[aá]ssio\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mEq/L', 3.5, 5.0,
     "Hipercalemia - risco arritmias", "Hipocalemia - fraqueza muscular"),
    ("Cálcio", "Cálcio sérico", r'[Cc]álcio\s+(?:s[eé]rico\s+)?[:=]?\s*([0-9]+[.,][0-9]+)', 'mg/dL', 8.5, 10.5,
     "Hipercalcemia", "Hipocalcemia"),
    ("Magnésio", "Magnésio", r'[Mm]agn[eé]sio\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mg/dL', 1.7, 2.2,
     "Hipermagnesemia", "Hipomagnesemia"),
    ("TSH", "TSH", r'TSH\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mUI/mL', 0.4, 4.0,
     "Hipotireoidismo subclínico", "Hipertireoidismo"),
    ("T4 livre", "T4 livre", r'(?:T4|t4)\s+[Ll]ivre\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'ng/dL', 0.8, 1.8,
     "Hipertireoidismo", "Hipotireoidismo"),
    ("Vitamina D", "Vitamina D", r'[Vv]itamina\s+D\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'ng/mL', 30.0, 100.0,
     "", "Deficiência de vitamina D"),
    ("Ferro sérico", "Ferro", r'[Ff]erro\s+(?:s[eé]rico\s+)?[:=]?\s*([0-9]+[.,][0-9]+)', 'µg/dL', 60.0, 170.0,
     "Sobrecarga de ferro", "Deficiência de ferro"),
    ("Ferritina", "Ferritina", r'[Ff]erritina\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'ng/mL', 12.0, 300.0,
     "Sobrecarga de ferro", "Deficiência de ferro"),
    ("Gama GT", "Gama GT", r'(?:Gama|Gamma)\s*GT\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'U/L', 5.0, 55.0,
     "Lesão hepatobiliar, uso de álcool, medicações", ""),
    ("Fosfatase alcalina", "Fosfatase alcalina", r'[Ff]osfatase\s+[Aa]lcalina\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'U/L', 30.0, 120.0,
     "Doença hepática, osseosa, gravidez", ""),
    ("PCR quantitativa", "PCR", r'(?:PCR|VHS|VES)\s*[:=]?\s*([0-9]+[.,][0-9]+)', 'mg/L', 0, 5.0,
     "Processo inflamatório / infeccioso", ""),
    ("VHS", "VHS", r'(?:VHS|VES)\s*[:=]?\s*([0-9]+)', 'mm/h', 0, 20.0,
     "Processo inflamatório agudo ou autoimune", ""),
    ("Urinálise", "Leucócitos urinários", r'[Ll]euc[oó]citos\s*[:=]?\s*([0-9]+)', '/campo', 0, 5.0,
     "Infecção urinária, pielonefrite", ""),
]

MODELOSATESTADO_DATA = [
    {
        'nome': 'Comparecimento Médico',
        'descricao': 'Atestado de comparecimento em consulta médica',
        'texto_template': (
            'ATESTADO DE COMPARECIMENTO MÉDICO\n\n'
            'A(o) Clínica {{clinica}}, abaixo assinada, atesta para os devidos fins '
            'que o(a) Sr(a). {{paciente}} compareceu a esta consulta médica no dia {{data_hoje}}.\n\n'
            'Local: {{local}}\n\n'
            'Atenciosamente,\n\n'
            '_________________________________\n'
            '{{medico}}\n'
            'CRM/CONSELHO\n'
        ),
        'requer_dias': False, 'requer_periodo': False, 'requer_cid': False,
    },
    {
        'nome': 'Afastamento do Trabalho',
        'descricao': 'Atestado de afastamento do trabalho por N dias',
        'texto_template': (
            'ATESTADO DE AFASTAMENTO DO TRABALHO\n\n'
            'A(o) Clínica {{clinica}} atesta para fins de afastamento do trabalho que o(a) Sr(a). '
            '{{paciente}} encontra-se impossibilitado(a) de realizar suas atividades laborais '
            'por um período de {{dias}} dia(s).\n\n'
            'Período: {{periodo}}\n\n'
            'CID-10: {{cid}}\n\n'
            'Local: {{local}}\n\n'
            'Atenciosamente,\n\n'
            '_________________________________\n'
            '{{medico}}\n'
            'CRM/CONSELHO\n'
        ),
        'requer_dias': True, 'requer_periodo': True, 'requer_cid': True,
    },
    {
        'nome': 'Comparecimento para Acompanhamento',
        'descricao': 'Atestado de comparecimento para acompanhamento de familiar',
        'texto_template': (
            'ATESTADO DE COMPARECIMENTO\n\n'
            'A(o) Clínica {{clinica}} atesta que o(a) Sr(a). {{paciente}} '
            'compareceu em {{data_hoje}} para acompanhamento de consulta médica de familiar.\n\n'
            'Local: {{local}}\n\n'
            'Atenciosamente,\n\n'
            '_________________________________\n'
            '{{medico}}\n'
            'CRM/CONSELHO\n'
        ),
        'requer_dias': False, 'requer_periodo': False, 'requer_cid': False,
    },
    {
        'nome': 'Retorno ao Trabalho',
        'descricao': 'Atestado de aptidão para retorno ao trabalho',
        'texto_template': (
            'ATESTADO DE RETORNO AO TRABALHO\n\n'
            'A(o) Clínica {{clinica}} atesta que o(a) Sr(a). {{paciente}} encontra-se '
            'apto(a) para retorno às suas atividades laborais a partir de {{data_hoje}}.\n\n'
            'CID-10: {{cid}}\n\n'
            'Local: {{local}}\n\n'
            'Atenciosamente,\n\n'
            '_________________________________\n'
            '{{medico}}\n'
            'CRM/CONSELHO\n'
        ),
        'requer_dias': False, 'requer_periodo': False, 'requer_cid': True,
    },
    {
        'nome': 'Aptidão para Atividade Física / Esportiva',
        'descricao': 'Atestado médico de aptidão para prática esportiva',
        'texto_template': (
            'ATESTADO DE APTIDÃO PARA ATIVIDADE FÍSICA\n\n'
            'A(o) Clínica {{clinica}} atesta que o(a) Sr(a). {{paciente}} '
            'encontra-se apto(a) para a prática de atividade física e/ou esportiva.\n\n'
            'Data do atestado: {{data_hoje}}\n\n'
            'Local: {{local}}\n\n'
            'Atenciosamente,\n\n'
            '_________________________________\n'
            '{{medico}}\n'
            'CRM/CONSELHO\n'
        ),
        'requer_dias': False, 'requer_periodo': False, 'requer_cid': False,
    },
    {
        'nome': 'Dispensa de Aula/Atividade',
        'descricao': 'Atestado para dispensa de atividades escolares ou extracurriculares',
        'texto_template': (
            'ATESTADO DE DISPENSA\n\n'
            'A(o) Clínica {{clinica}} atesta que o(a) Sr(a). {{paciente}} '
            'não poderá comparecer a atividades escolares/extracurriculares '
            'no período de {{periodo}}, totalizando {{dias}} dia(s).\n\n'
            'CID-10: {{cid}}\n\n'
            'Local: {{local}}\n\n'
            'Atenciosamente,\n\n'
            '_________________________________\n'
            '{{medico}}\n'
            'CRM/CONSELHO\n'
        ),
        'requer_dias': True, 'requer_periodo': True, 'requer_cid': False,
    },
]

# Base de conhecimento clínica: (condição nome, cid, [(sintoma, peso)], [(exame, peso, "")], [(medicamento, peso, "posologia")])
BASE_CONHECIMENTO = [
    {
        'condicao': 'Infecção do Trato Urinário (ITU)',
        'cid': 'N39.0',
        'sintomas': [
            ('Disúria', 2.0), ('Polaciúria', 2.0), ('Urgência urinária', 1.5),
            ('Dor lombar baixa', 1.0), ('Febre baixa', 0.8), ('Urina turva', 0.7),
            ('Hematúria', 0.6), ('Mal-urinário', 0.5),
        ],
        'exames': [
            ('Urinálise', 2.0), ('Urocultura', 2.0), ('Antibiograma', 1.5),
        ],
        'medicamentos': [
            ('Nitrofurantoína', 2.0, '100mg 12/12h por 5-7 dias'),
            ('Ciprofloxacino', 1.5, '500mg 12/12h por 7 dias'),
            ('Sulfametoxazol + Trimetoprima', 1.5, '480mg 12/12h por 7 dias'),
        ],
    },
    {
        'condicao': 'Hipertensão Arterial Sistêmica',
        'cid': 'I10',
        'sintomas': [
            ('Cefaleia', 1.5), ('Tontura', 1.0), ('Dor de cabeça matinal', 1.2),
            ('Zumbido', 0.8), ('Dispneia aos esforços', 0.6), ('Dor torácica', 0.5),
        ],
        'exames': [
            ('Hemograma completo', 1.0), ('Creatinina', 1.5), ('Ureia', 1.0),
            ('Sódio', 1.0), ('Potássio', 1.0), ('Eletrocardiograma (ECG)', 1.5),
            ('Mapa 24h', 2.0), ('Urinálise', 1.0),
        ],
        'medicamentos': [
            ('Losartana', 2.0, '50mg 1x/dia'),
            ('Anlodipino', 1.8, '5mg 1x/dia'),
            ('Enalapril', 1.5, '10mg 1x/dia'),
            ('Hidroclorotiazida', 1.2, '25mg 1x/dia'),
            ('Bisoprolol', 1.0, '5mg 1x/dia'),
        ],
    },
    {
        'condicao': 'Diabetes Mellitus Tipo 2',
        'cid': 'E11',
        'sintomas': [
            ('Poliúria', 1.8), ('Polidipsia', 1.8), ('Perda de peso', 1.2),
            ('Fadiga', 1.0), ('Visão embaçada', 1.0), ('Formigamento nos pés', 0.8),
            ('Cicatrização lenta', 0.7),
        ],
        'exames': [
            ('Glicemia de jejum', 2.0), ('HbA1c (Hemoglobina glicada)', 2.0),
            ('HOMA-IR', 1.0), ('Colesterol total', 1.0), ('HDL', 1.0),
            ('LDL', 1.0), ('Triglicerídeos', 1.0), ('Creatinina', 1.0),
        ],
        'medicamentos': [
            ('Metformina', 2.0, '500mg 2x/dia, após refeições'),
            ('Gliclazida', 1.2, '30mg 1x/dia pela manhã'),
        ],
    },
    {
        'condicao': 'Infecção Respiratória Aguda (IRA)',
        'cid': 'J06.9',
        'sintomas': [
            ('Febre', 2.0), ('Tosse', 2.0), ('Dor de garganta', 1.5),
            ('Coriza', 1.2), ('Congestão nasal', 1.0), ('Cefaleia', 0.8),
            ('Mal-estar', 0.7), ('Otalgia', 0.5),
        ],
        'exames': [
            ('Hemograma completo', 1.0), ('PCR quantitativa', 1.2),
        ],
        'medicamentos': [
            ('Paracetamol', 2.0, '750mg 6/6h por 5 dias'),
            ('Ibuprofeno', 1.2, '400mg 8/8h por 3-5 dias'),
            ('Ambroxol', 1.0, '75mg 1x/dia por 5 dias'),
            ('Azitromicina', 0.8, '500mg 1x/dia por 3 dias (se suspeita bacteriana)'),
        ],
    },
    {
        'condicao': 'Lombalgia / Dor Lombar',
        'cid': 'M54.5',
        'sintomas': [
            ('Dor lombar baixa', 3.0), ('Limitação de movimentos', 1.5),
            ('Rigidez lombar', 1.2), ('Irradiação para membro inferior', 1.0),
            ('Dor ao levantar', 0.8),
        ],
        'exames': [
            ('Raio-X de coluna', 1.5), ('Ressonância de coluna', 1.0),
        ],
        'medicamentos': [
            ('Diclofenaco', 2.0, '75mg gotas 12/12h por 5-7 dias'),
            ('Dipirona', 1.5, '1g 6/6h se dor'),
            ('Nimesulida', 1.2, '100mg 12/12h por 5 dias'),
            ('Diazepam', 0.5, '5mg 8/8h por 3 dias (se espasmo muscular)'),
        ],
    },
    {
        'condicao': 'Dor Torácica de Origem Musculoesquelética',
        'cid': 'M54.6',
        'sintomas': [
            ('Dor torácica', 2.0), ('Dor ao respirar fundo', 1.5),
            ('Dor ao palpar', 1.5), ('Dor ao movimento', 1.0),
        ],
        'exames': [
            ('Eletrocardiograma (ECG)', 2.0), ('Raio-X de tórax', 1.5),
            ('Troponina', 1.5), ('CK-MB', 1.0),
        ],
        'medicamentos': [
            ('Diclofenaco', 2.0, '50mg 8/8h por 5 dias'),
            ('Dipirona', 1.5, '1g 6/6h se dor'),
        ],
    },
    {
        'condicao': 'Gastroenterite Aguda',
        'cid': 'A09',
        'sintomas': [
            ('Diarreia', 2.0), ('Náusea', 2.0), ('Vômitos', 1.8),
            ('Cólica abdominal', 1.5), ('Febre baixa', 0.8), ('Desidratação', 1.0),
        ],
        'exames': [
            ('Urinálise', 1.0), ('Hemograma completo', 1.0),
            ('Ecoparasitológico', 0.8), ('Sódio', 0.8), ('Potássio', 0.8),
        ],
        'medicamentos': [
            ('Dipirona', 1.0, '1g 6/6h se febre/dor'),
            ('Omeprazol', 1.2, '20mg 1x/dia pela manhã'),
            ('Metoclopramida', 1.0, '10mg 8/8h antes das refeições'),
        ],
    },
    {
        'condicao': 'Ansiedade',
        'cid': 'F41.1',
        'sintomas': [
            ('Ansiedade', 3.0), ('Insônia', 1.5), ('Palpitação', 1.2),
            ('Tensão muscular', 1.0), ('Sudorese', 0.8), ('Irritabilidade', 0.8),
            ('Dificuldade de concentração', 0.7),
        ],
        'exames': [
            ('TSH', 1.0), ('T4 livre', 0.8), ('Hemograma completo', 0.5),
            ('Eletrocardiograma (ECG)', 0.8),
        ],
        'medicamentos': [
            ('Escitalopram', 2.0, '10mg 1x/dia pela manhã'),
            ('Sertralina', 1.8, '50mg 1x/dia pela manhã'),
            ('Alprazolam', 1.0, '0.25mg 8/8h se ansiedade intensa (curto prazo)'),
        ],
    },
    {
        'condicao': 'Faringite Aguda',
        'cid': 'J02.9',
        'sintomas': [
            ('Dor de garganta', 3.0), ('Odinofagia', 2.0), ('Febre', 1.5),
            ('Cefaleia', 0.8), ('Catarro', 0.5),
        ],
        'exames': [
            ('Hemograma completo', 1.0), ('PCR quantitativa', 1.2),
        ],
        'medicamentos': [
            ('Amoxicilina', 1.5, '500mg 8/8h por 10 dias (se origem bacteriana)'),
            ('Azitromicina', 1.5, '500mg 1x/dia por 3-5 dias'),
            ('Paracetamol', 2.0, '750mg 6/6h por 5 dias'),
            ('Dipirona', 1.5, '1g 6/6h se febre/dor'),
        ],
    },
    {
        'condicao': 'Asma',
        'cid': 'J45',
        'sintomas': [
            ('Dispneia', 2.0), ('Sibilância', 2.5), ('Tosse noturna', 1.5),
            ('Aperto no peito', 1.5), ('Dispneia ao esforço', 1.2),
        ],
        'exames': [
            ('Espirometria', 2.0), ('Raio-X de tórax', 1.0),
            ('Eosinófilos (hemograma)', 0.8), ('IgE total', 0.5),
        ],
        'medicamentos': [
            ('Salbutamol', 2.0, '2 jatos ao sintoma (bom alívio)'),
            ('Budesonida', 1.8, '200mcg 2x/dia inalatório'),
            ('Fluticasona', 1.5, '250mcg 2x/dia inalatório'),
            ('Montelucaste', 1.0, '10mg 1x/dia à noite'),
        ],
    },
    {
        'condicao': 'Insônia Primária',
        'cid': 'G47.0',
        'sintomas': [
            ('Insônia', 3.0), ('Dificuldade para dormir', 2.0),
            ('Despertar frequente', 2.0), ('Sonolência diurna', 1.5),
            ('Fadiga', 1.0), ('Irritabilidade', 0.8),
        ],
        'exames': [],
        'medicamentos': [
            ('Melatonina', 1.5, '3mg 30min antes de dormir'),
            ('Diazepam', 1.0, '5mg ao deitar (curto prazo)'),
            ('Rivotril', 0.8, '0.5mg ao deitar (curto prazo)'),
        ],
    },
    {
        'condicao': 'Hipotireoidismo',
        'cid': 'E03.9',
        'sintomas': [
            ('Fadiga', 1.5), ('Ganho de peso', 1.5), ('Intolerância ao frio', 2.0),
            ('Pele seca', 1.2), ('Constipação', 1.0), ('Queda de cabelo', 0.8),
            ('Depressão', 0.7), ('Edema', 0.6),
        ],
        'exames': [
            ('TSH', 2.5), ('T4 livre', 2.5), ('Anti-TPO', 1.0),
            ('Colesterol total', 0.8), ('Triglicerídeos', 0.5),
        ],
        'medicamentos': [
            ('Levotiroxina', 2.5, '50-100mcg 1x/dia em jejum, 30min antes do café'),
        ],
    },
    {
        'condicao': 'Osteoartrose',
        'cid': 'M15-M19',
        'sintomas': [
            ('Dor articular', 2.5), ('Rigidez matinal', 1.5),
            ('Limitação de movimentos', 1.5), ('Crujar articular', 1.0),
            ('Edema articular', 0.8),
        ],
        'exames': [
            ('Raio-X de articulação', 2.0), ('Hemograma completo', 0.5),
            ('VHS', 0.5), ('PCR quantitativa', 0.5),
        ],
        'medicamentos': [
            ('Ibuprofeno', 2.0, '400mg 8/8h por 7-14 dias'),
            ('Diclofenaco', 1.8, '50mg 8/8h por 7 dias'),
            ('Piroxicam', 1.5, '20mg 1x/dia com alimento'),
        ],
    },
]


class Command(BaseCommand):
    help = 'Popula catálogos de exames, medicamentos, modelos de atestado e base de conhecimento.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help='Apaga todos os dados existentes antes de semear (USE COM CUIDADO)'
        )

    def handle(self, *args, **options):
        from exames.models import Exame, ValorReferencia
        from receituario.models import Medicamento
        from atestados.models import ModeloAtestado
        from sugestoes.models import Sintoma, Condicao, SintomaCondicao, CondicaoExameSugerida, CondicaoMedicamentoSugerido

        if options['reset']:
            self.stdout.write(self.style.WARNING('Apagando dados existentes...'))
            for m in [ValorReferencia, Exame, Medicamento, ModeloAtestado,
                      CondicaoExameSugerida, CondicaoMedicamentoSugerido,
                      SintomaCondicao, Condicao, Sintoma]:
                m.objects.all().delete()

        # ── Exames ──
        exames_criados = 0
        for nome, categoria, preparo in CATALOGO_EXAMES:
            _, created = Exame.objects.get_or_create(
                nome=nome, defaults={'categoria': categoria, 'preparo': preparo}
            )
            exames_criados += int(created)
        self.stdout.write(f'  ✓ {exames_criados} exames criados (de {len(CATALOGO_EXAMES)} no catálogo)')

        # ── Valores de Referência ──
        vr_criados = 0
        for exame_nome, analito, padrao, unidade, vmin, vmax, alt, bai in VALORES_REFERENCIA:
            try:
                exame = Exame.objects.get(nome=exame_nome)
                _, created = ValorReferencia.objects.get_or_create(
                    exame=exame, analito=analito,
                    defaults={
                        'padrao_busca': padrao, 'unidade': unidade,
                        'valor_min': vmin, 'valor_max': vmax,
                        'orientacao_alto': alt, 'orientacao_baixo': bai,
                    }
                )
                vr_criados += int(created)
            except Exame.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Exame "{exame_nome}" não encontrado para valor de referência'))
        self.stdout.write(f'  ✓ {vr_criados} valores de referência criados')

        # ── Medicamentos ──
        meds_criados = 0
        for nome, principio, apresentacoes in CATALOGO_MEDICAMENTOS:
            _, created = Medicamento.objects.get_or_create(
                nome=nome, defaults={'principio_ativo': principio, 'apresentacoes': apresentacoes}
            )
            meds_criados += int(created)
        self.stdout.write(f'  ✓ {meds_criados} medicamentos criados (de {len(CATALOGO_MEDICAMENTOS)} no catálogo)')

        # ── Modelos de Atestado ──
        at_criados = 0
        for dados in MODELOSATESTADO_DATA:
            _, created = ModeloAtestado.objects.get_or_create(
                nome=dados['nome'], defaults=dados
            )
            at_criados += int(created)
        self.stdout.write(f'  ✓ {at_criados} modelos de atestado criados')

        # ── Base de Conhecimento ──
        sintomas_criados = 0
        condicoes_criadas = 0
        relacoes_sc = 0
        relacoes_ce = 0
        relacoes_cm = 0

        for item in BASE_CONHECIMENTO:
            cond, _ = Condicao.objects.get_or_create(
                nome=item['condicao'], defaults={'cid': item.get('cid', '')}
            )
            condicoes_criadas += int(_)

            for nome_sint, peso in item['sintomas']:
                s, _ = Sintoma.objects.get_or_create(nome=nome_sint)
                sintomas_criados += int(_)
                _, _ = SintomaCondicao.objects.get_or_create(
                    sintoma=s, condicao=cond, defaults={'peso': peso}
                )
                relacoes_sc += 1

            for exame_info in item['exames']:
                exame_nome, peso = exame_info[0], exame_info[1]
                try:
                    exame = Exame.objects.get(nome=exame_nome)
                    _, _ = CondicaoExameSugerida.objects.get_or_create(
                        condicao=cond, exame=exame, defaults={'peso': peso}
                    )
                    relacoes_ce += 1
                except Exame.DoesNotExist:
                    pass

            for med_info in item['medicamentos']:
                med_nome, peso = med_info[0], med_info[1]
                posologia = med_info[2] if len(med_info) > 2 else ''
                try:
                    med = Medicamento.objects.get(nome=med_nome)
                    _, _ = CondicaoMedicamentoSugerido.objects.get_or_create(
                        condicao=cond, medicamento=med,
                        defaults={'peso': peso, 'posologia_sugerida': posologia}
                    )
                    relacoes_cm += 1
                except Medicamento.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  Medicamento "{med_nome}" não encontrado para conhecimento'))

        self.stdout.write(f'  ✓ {len(BASE_CONHECIMENTO)} condições, {sintomas_criados} sintomas, '
                          f'{relacoes_sc} sint→cond, {relacoes_ce} cond→exame, {relacoes_cm} cond→med')
        self.stdout.write(self.style.SUCCESS('Sementeira concluída com sucesso!'))
