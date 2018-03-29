
//var btn = document.createElement('input');
//btn.type = "button";
//btn.className = "btn";
//btn.onclick = (function(entry) {return function() {chooseUser(entry);}})(entry);

var placeholderCellCss = "border: none;";

function closeWindow(winName){
    console.log("CLOSED " +  winName);
    jQuery.ajax({
        type: "POST", 
        url: $SCRIPT_ROOT + "/closewin",  
        data: JSON.stringify({
            name: winName
        }),
        contentType: 'application/json;charset=UTF-8',
        success: function(response){
            // do something
        }
    })
}

function updateWinTable() {
    $("#window_table").empty();
    $.getJSON($SCRIPT_ROOT + "/jstats", function (data) {
        console.log(data["Windows"])
        var tbl_body = document.createElement("tbody");
        $.each(data["Windows"], function (k, v) {
            //Start adding loop
            var btn_tbl_row = tbl_body.insertRow();
            var tbl_row = tbl_body.insertRow();
            var btncell = tbl_row.insertCell();
            btncell.style.cssText = "border:none; border-top: 1px solid black;";
            var cell = tbl_row.insertCell();
            
            //Create button
            var btn = document.createElement("button");
            btn.type = "button";
            btn.innerText = "X";
            btn.className = "btn";
            btn.style.cssText = "border: 1px solid black; background-color:red;height: 20px;color:white";
            btncell.appendChild(btn);
            btn.addEventListener('click', function(){
                closeWindow(v["Window_name"].toString());
                
            });
            //btn.onclick = closeWindow(v["Window_name"].toString());
            //End button creation
            cell.append("Window Name: ")
            //cell.style.cssText = "padding-left: 30px;";
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["Window_name"].toString()));
            //End adding loop
            var tbl_row = tbl_body.insertRow();
            var cell = tbl_row.insertCell();
            cell.style.cssText = placeholderCellCss;
            var cell = tbl_row.insertCell();
            
            cell.append("X: ")
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["X"].toString()));
            //Start adding loop
            var tbl_row = tbl_body.insertRow();
            var cell = tbl_row.insertCell();
            cell.style.cssText = placeholderCellCss;
            var cell = tbl_row.insertCell();
            cell.append("Y: ")
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["Y"].toString()));
            var tbl_row = tbl_body.insertRow();
            var cell = tbl_row.insertCell();
            cell.style.cssText = placeholderCellCss;
            var cell = tbl_row.insertCell();
            cell.append("Width: ")
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["Width"].toString()));
            var tbl_row = tbl_body.insertRow();
            var cell = tbl_row.insertCell();
            cell.style.cssText = placeholderCellCss;
            var cell = tbl_row.insertCell();
            cell.append("Height: ")
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["Height"].toString()));
        })

        $("#window_table").append(tbl_body);
    });
}
function updateDiskTable() {
    $("#disk_table").empty();
    $.getJSON($SCRIPT_ROOT + "/jstats", function (data) {
        //console.log(data)
        var tbl_body = document.createElement("tbody");
        var html = ""
        $.each(data["Disks"], function (k, v) {
            //html += '<tr><td>data from json</td></tr>';
            
            //Start adding loop
            var tbl_row = tbl_body.insertRow();
            var cell = tbl_row.insertCell();
            cell.append("Device: ")
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["Device"].toString()));
            //End adding loop
            //Start adding loop
            console.log(v)
            var tbl_row = tbl_body.insertRow();
            var cell = tbl_row.insertCell();
            cell.append("Disk Size: ")
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["Disk size"].toString()));
            //Start adding loop
            console.log(v)
            var tbl_row = tbl_body.insertRow();
            var cell = tbl_row.insertCell();
            cell.append("Used: ")
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["Used"].toString()));
            //Start adding loop
            console.log(v)
            var tbl_row = tbl_body.insertRow();
            var cell = tbl_row.insertCell();
            cell.append("Free: ")
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["Free"].toString()));
            //Start adding loop
            console.log(v)
            var tbl_row = tbl_body.insertRow();
            var cell = tbl_row.insertCell();
            cell.append("Percent used: ")
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["Percent used"].toString()));
            //Start adding loop
            console.log(v)
            var tbl_row = tbl_body.insertRow();
            var cell = tbl_row.insertCell();
            cell.append("fstype: ")
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["fstype"].toString()));
            //Start adding loop
            console.log(v)
            var tbl_row = tbl_body.insertRow();
            var cell = tbl_row.insertCell();
            cell.append("Mount point: ")
            var cell = tbl_row.insertCell();
            cell.appendChild(document.createTextNode(v["Mount point"].toString()));
            
        })

        $("#disk_table").append(tbl_body);
    });
}

function updateCPUTable(points) {
    $.getJSON($SCRIPT_ROOT + "/jstats", function (data) {
        //console.log(data["CPU"][0]["CPU Percent"])
        console.log("POINTS: " + points)
        var canvas = document.getElementById("chartContainer");
        var data = {
            labels: points,
            datasets: [
                {
                    label: "CPU %",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(75,192,192,0.4)",
                    borderColor: "rgba(75,192,192,1)",
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: "rgba(75,192,192,1)",
                    pointBackgroundColor: "#fff",
                    
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    
                    data: points,
                }]
        };

        var myLineChart = new Chart(canvas, {
            type: 'line',
            data: data,
            options: {
                animation: {
                    duration: 0, // general animation time
                },
                hover: {
                    animationDuration: 0, // duration of animations when hovering an item
                },
                responsiveAnimationDuration: 0, // animation duration after a resize
            }

        });
        myLineChart.update()



    })
}

//TODO: Decide if the cpu temps should be in a table or as a graph. 
//      Graph is kinda ugly... I also gotta check for num of cores and everything...
//      Maybe I'll just not include CPU temps... Seems like kind of a fuss.
function updateCPUTempTable(points0, points1, points2, points3) {
    $.getJSON($SCRIPT_ROOT + "/jstats", function (data) {
        //console.log(data["CPU"][0]["CPU Percent"])
        console.log("POINTS: " + points0)
        var canvas = document.getElementById("chartContainerTemps");
        var data = {
            labels: points0,
            datasets: [
                {
                    label: "Core 0",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(75,192,192,0.4)",
                    borderColor: "black",
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: "rgba(75,192,192,1)",
                    pointBackgroundColor: "#fff",
                    
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    
                    data: points0,
                }, {
                    label: "Core 1",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(75,192,192,0.4)",
                    borderColor: "blue",
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: "rgba(75,192,192,1)",
                    pointBackgroundColor: "#fff",
                    
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    
                    data: points1,
                }, {
                    label: "Core 2",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(75,192,192,0.4)",
                    borderColor: "red",
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: "rgba(75,192,192,1)",
                    pointBackgroundColor: "#fff",
                    
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    
                    data: points2,
                }, {
                    label: "Core 3",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(75,192,192,0.4)",
                    borderColor: "green",
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: "rgba(75,192,192,1)",
                    pointBackgroundColor: "#fff",
                    
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    
                    data: points3,
                }]
        };

        var myLineChart = new Chart(canvas, {
            type: 'line',
            data: data,
            options: {
                animation: {
                    duration: 0, // general animation time
                },
                hover: {
                    animationDuration: 0, // duration of animations when hovering an item
                },
                responsiveAnimationDuration: 0, // animation duration after a resize
            }

        });
        myLineChart.update()



    })
}
