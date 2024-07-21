
let timer = false;
let hour = 0; 
let minute = 0; 
let second = 0; 
let count = 0; 


document.onreadystatechange = () => {
    if (document.readyState === "complete") {
    	timer = true; 
		stopWatch(); 
    }
  };


function stopWatch() { 
	if (timer) { 
		count++; 
		
		if (count == 100) { 
			second++; 
			count = 0; 
		} 

		if (second == 60) { 
			minute++; 
			second = 0; 
		} 

		if (minute == 60) { 
			hour++; 
			minute = 0; 
			second = 0; 
		} 
		
		hrString = hour; 
		minString = minute; 
		secString = second; 
		countString = count; 
		if (hour < 10) { 
			hrString = "0" + hrString; 
		} 

		if (minute < 10) { 
			minString = "0" + minString; 
		} 

		if (second < 10) { 
			secString = "0" + secString; 
		} 

		

		document.getElementById('hr').innerHTML = hrString; 
		document.getElementById('min').innerHTML = minString; 
		document.getElementById('sec').innerHTML = secString; 
		setTimeout(stopWatch, 10); 
	} 
}

