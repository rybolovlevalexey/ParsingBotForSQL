import pandas as pd

BRANDS = sorted(['Terios', 'Great Wall', 'Nissan', 'KIA', 'Subaru', 'BYD', 'KJ',
                 'Марка не опознана',
                 'MOSKVICH', 'Suzuki', 'SOLLERS', 'Ssang yong', 'Прицеп', 'CHEVROLET',
                 'UAZ', 'Мотоцикл', 'INFINITI', 'Skoda', 'BMW', 'HARLEY DAVIDSON',
                 'МОСКВИЧ', 'RENAULT', 'HONDA', 'FORD', 'CHANGAN', 'MITSUBISHI',
                 'Tesla', 'Катер', 'CHRYSLER', 'Audi', 'DAEWOO', 'Ferrari', 'DODGE',
                 'GAC', 'Fiat', 'CHERY', 'LIFAN', 'HAVAL', 'ГАЗ', 'ZAZ', 'SKODA', 'Citroen',
                 'HYUNDAI',
                 'Lexus', 'JEEP', 'LADA', 'Daihatsu', 'OPEL', 'OMODA', 'Maserati', 'KAIYI', 'ВАЗ',
                 'MERCEDES-BENZ', 'Datsun', 'УАЗ', 'MAZDA', 'JETOUR', 'HUSQVARNA',
                 'Mercedes', 'ЗАЗ', 'Zeekr', 'RENO', 'АФ', 'GENESIS',
                 'MINI COOPER', 'RAVON', 'Volkswagen', 'JAGUAR', 'VOGE', 'Volga', 'TOYOTA', 'Seat',
                 'GEELY', 'Volvo', 'Land Rover', 'CADILLAC', 'ГАС', 'JAECOO', 'Vortex',
                 'КВАДРОЦИКЛ', 'Bentley', 'KTM', 'JETTA', 'Peugeot', 'Avatr', 'Porsche', 'Alfa'])

QUESTIONS_SYSTEM = {
    "start": "QUES_SYS{0};",
    1: {"text": "Данный файл подходит под шаблон бренда {0}. Указанный файл от этого бренда?",
        "answers": ["Да", "Нет"]},
    2: {},
    3: {}
}

#df = pd.read_excel("files with costs/@@PriceList_Changes_01_10_2023.xlsx")
#sp = list(list(df.iterrows())[0][1].keys())
#print(sp)
#for elem in list(df.iterrows())[0][1]:
#    print(elem)
#