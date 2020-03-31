function getAPI()
			{
				(async () => {
				   let response = await new Promise(resolve => {
					  var xhr = new XMLHttpRequest();
					  xhr.open("GET", "http://api.postcodes.io/postcodes/"+document.getElementById('customInput').value, true);
					  xhr.onload = function(e) {
						var myObj = JSON.parse(this.responseText);
						document.getElementById('id_outward').value = myObj.result.outcode;
						resolve(xhr.response);
					  };
					  xhr.onerror = function () {
						resolve(undefined);
						console.error("** An error occurred during the XMLHttpRequest");
					  };
					  xhr.send();
				   }) 
				   getNeighbourhood();
				   getNearestPostCodes();	
				})()			
			};
			


			function getOutward() {
			  var xhttp = new XMLHttpRequest();
			  xhttp.onreadystatechange = function() {
				if (this.status == 200) {
				var myObj = JSON.parse(this.responseText);
				document.getElementById('id_outward').value = myObj.result.outcode;
				}
			  };
			  xhttp.open("GET", "http://api.postcodes.io/postcodes/"+document.getElementById('id_postcode').value,true);
			  xhttp.send();
			};
			
			function getNeighbourhood() {
			  var xhttp = new XMLHttpRequest();
			  xhttp.onreadystatechange = function() {
				if (this.status == 200) {
				var myObj = JSON.parse(this.responseText);
					document.getElementById('id_neighbour').value = myObj.result.admin_ward;
				}
			  };
			  xhttp.open("GET", "http://api.postcodes.io/outcodes/"+document.getElementById('id_outward').value);
			  xhttp.send();
			};
			
			function getNearestPostCodes() {
			  var xhttp = new XMLHttpRequest();
			  xhttp.onreadystatechange = function() {
				if (this.status == 200) {
				var myObj = JSON.parse(this.responseText);
					var outcodes="";
					var i;
					for(i=0;i<5;i++)
					{
					outcodes+=myObj.result[i].outcode+", ";
					}
					document.getElementById('id_nearest').value=outcodes;
				}
			  };
			  xhttp.open("GET", "http://api.postcodes.io/outcodes/"+document.getElementById('id_outward').value+"/nearest");
			  xhttp.send();
			};

			function updateImage() {
				var i;
				
				for(i = 0; i<2; i++)
				{
				if (document.getElementById("id_form-"+i+"-image").value!='')
				{
				$("#id_form-"+(i+1)+"-image").show();
				$("#img"+(i+1)).show();
				}
				}
			}
			function hide()
			
			{
				var i;
				
				for(i = 1; i<3; i++)
				{
				$("#id_form-"+(i)+"-image").hide();
				$("#img"+(i)).hide();
				}
			}
			
			
			function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
				var i = 0;
				i=input.id.match(/\d+/g);
                reader.onload = function (e) {
                    $('#img'+i)
                        .attr('src', e.target.result);
                };

                reader.readAsDataURL(input.files[0]);
            }
        }