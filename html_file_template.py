
def edit_html_body(fil_cat,fil_year,table_content,category_dropdown,year_dropdown):

    html_body = f'''<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <link
                rel="stylesheet"
                href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"
            />
            <title>Noble Price Winner | 17MIS0122</title>
        </head>
        <body>
            <div class="container">
                <h1 style="text-align: center">Noble Price List<br><h4 style="text-align: center">Category: <b>{fil_cat}</b>,Year: <b>{fil_year}</b></h4></h1>
                <div class="row">
                    <div class="nine columns">
                        <table width="100%">
                            <thead>
                                <tr>
                                    <th>Year</th>
                                    <th>Id</th>
                                    <th>First Name</th>
                                    <th>Surname</th>
                                    <th>Category</th>
                                    <th>Motivation</th>
                                    <th>Share</th>
                                </tr>
                            </thead>
                            <tbody>
                                {table_content}
                            </tbody>
                        </table>
                    </div>
                    <div class="three columns">
                        <h3>Filters</h3>
                        <h6>To view by Category</h6>
                        <form action="/naraen/noblelaureates/api/">
                            <select name="category" id="category">
                                {category_dropdown}
                            </select>
                            <h6>To view by Year</h6>
                            <select name="year" id="year">
                                {year_dropdown}
                            </select>
                            <br />
                            <input type="submit" value="Submit Request" />
                        </form>
                        <form action="/naraen/topnoblelaureates/api/">
                        <h5>
                            To view people who have won the noble price more than
                            once please
                        </h5>
                        <input type="submit" value="Click Here" />
                        </form>
                    </div>
                </div>
            </div>
        </body>
    </html>
    '''

    return html_body