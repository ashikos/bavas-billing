def post(self, *args, **kwargs):
    data = self.request.data
    excel_file = data['excel']
    date = data['date']

    # try:
    for day in range(1, 32):
        print("==============")
        date = f'{day}-12-2023'
        print('date', date)
        date_object = datetime.strptime(date, "%d-%m-%Y").date()
        # sheet_name = str(date_object.day)

        sheet_name = str(day)  # remove after excel bulk excel upload

        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        df = df.where(pd.notnull(df), None)

        for row in range(1, 50):

            if pd.isna(df.iloc[row, 0]):
                break

            data = {
                "reg_no": df.iloc[row, 1] if not pd.isna(
                    df.iloc[row, 1]) else None,
                "mob": df.iloc[row, 2] if not pd.isna(
                    df.iloc[row, 2]) else None,
                "vehicle": df.iloc[row, 3] if not pd.isna(
                    df.iloc[row, 3]) else None,
                "service_type": df.iloc[row, 4] if not pd.isna(
                    df.iloc[row, 4]) else None,
            }
            print('data', data)
            if any(value and not str(value).isspace() for value in
                   data.values()):
                entry, created = bill_models.Entries.objects.get_or_create(
                    reg_no=data['reg_no'], date=date_object,
                    contact=data['mob'])

                entry.vehicle = data['vehicle']
                entry.type = data['service_type']

                amount, gpay, is_credit_received = Check_amount_type(
                    df, row)
                print('amiont', amount, gpay)
                entry.amount = amount
                entry.gpay = gpay
                entry.is_credit_received = is_credit_received
                entry.date = date_object

                entry.save()
                ids = entry.id
                ent = bill_models.Entries.objects.get(id=ids)
        # except:
        #     raise Bad_Request("Invalid excel uploded")

    return Response("excel uploaded succesfully")