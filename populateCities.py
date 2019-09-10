def popCities():

    import pandas as pd
    from Estabelecimento.models import Cidade


    path = 'C:\\Users\\vini2\\Desktop\\JJP Data Intelligence\\Projetos\\Projetos Ativos\\Guia Comercial Brasil\\Novo GCB\\Documentos\\municipios.csv'
    df = pd.read_csv(path, sep = ';').dropna()

    for index, row in df.iterrows():
        pais = row['Pais']
        estado = row['Estado']
        cidade = row['Cidade']
        
        Cidade.objects.create(pais = pais, estado = estado, cidade = cidade)

        print("Row {} out of {} Recorded.".format(index, len(df.index)))

    input('END OF SCRIPT. ENTER ANY KEY TO EXIT...')