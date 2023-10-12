console.log("dashboard.js");

city_dropdown = d3.select("#city")

city_dropdown
    .append("option")
    .text("Pick one")
    .property("value", 0);

d3.json("http://127.0.0.1:5000/api/city_count").then(function (data) {
    // console.log(data)

    for (i = 0; i < data.length; i++) {
        city_dropdown
            .append("option")
            .text(data[i].city)
            .property("value", data[i].city);

    }

    build_pie_chart(data)

})

function build_pie_chart(data) {
    // console.log("build_pie_chart")
    // console.log(data)

    city_list = []
    count_list = []

    for (i = 0; i < data.length; i++) {
        city_list.push(data[i].city)
        count_list.push(data[i].count)
    }

    var data = [{
        values: count_list,
        labels: city_list,
        type: 'pie'
    }];

    var layout = {
        height: 400,
        width: 500
    };

    Plotly.newPlot('pieChart', data, layout);

}

function optionChanged(city) {
    console.log("optionChanged")
    console.log(city)

    d3.json("http://127.0.0.1:5000/api/job_category/" + city).then(function (data) {
        // console.log(data)

        type_list = []
        count_list = []

        for (i = 0; i < data.length; i++) {
            type_list.push(data[i].title)
            count_list.push(data[i].count)
        }

        var data = [{
            values: count_list,
            labels: type_list,
            type: 'pie'
        }];

        var layout = {
            height: 400,
            width: 500
        };

        Plotly.newPlot('pieChart', data, layout);

    })

    const tbody = d3.select("tbody");

    d3.json("http://127.0.0.1:5000/api/job_info/" + city).then(function (data) {
        // console.log(data)

        tbody.html("");

        const tbl_header = tbody.append("tr");

        let header = tbl_header.append("th");
        header.text('City');
        header = tbl_header.append("th");
        header.text('Company Name');
        header = tbl_header.append("th");
        header.text('Company Type');
        header = tbl_header.append("th");
        header.text('Job Type');
        header = tbl_header.append("th");
        header.text('Job Title');
        header = tbl_header.append("th");
        header.text('Remote');
        

        data.forEach((row) => {
            // Create tr for each row of the table
            const tbl_data = tbody.append("tr");

            console.log("row")
            console.log(row)

            //Create multiple td cells for each row
            Object.values(row).forEach((value) => {
                let cell = tbl_data.append("td");
                cell.text(value);
            });
        });
    })
}    