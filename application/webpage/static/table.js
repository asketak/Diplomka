

						var processingComplete = function(){};
						$('#my-final-table').dynatable({
							dataset: {
								records: tabledata
							}
						}).bind('dynatable:afterProcess', processingComplete);

// call the first time manually
processingComplete();

$('#my-final-table hr').on("click",function(){
});