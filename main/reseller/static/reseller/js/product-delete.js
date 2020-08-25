(function($){
	window.delete_product = function (id){
		$(document).on("click","#delete-"+id , function (e) {
			Swal.fire({
				title: 'Are you sure?',
				text: "You won't be able to login from this device till you approve it again",
				type: 'warning',
				showCancelButton: true,
				confirmButtonColor: '#3085d6',
				cancelButtonColor: '#d33',
				confirmButtonText: 'Yes, delete it!'
			}).then((result) => {
				var url = "{% url 'reseller:delete_product' %}";
				if (result.value) {
					$.post( url, { csrfmiddlewaretoken: '{{ csrf_token }}', id: id }, function( data ) {
						if (data.status){
							Swal.fire(
								'Deleted!',
								'The Device has been deleted.',
								'success'
							)
							$('#product-'+id).remove();
						}
						else{
							Swal.fire(
								'Error!',
								'Error while deleting your device',
								'Error'
							)
						}
					});					
				}
			})
		});
	};
})(jQuery);