var PFGSOUP_asInitVals = new Array();

(function($) {
	$(document).ready(function() {
		var url = $('#pfgsoupdata').attr('data-ajaxurl');
		var oTable = $('#pfgsoupdata').dataTable( {
			"bProcessing": true,
			"bServerSide": true,
			"sAjaxSource": url,
			"sPaginationType": "full_numbers",
			'fnDrawCallback' : function(oSettings) {
				$("#pfgsoupdata tbody a.pfgsoup-edit").click(function() {
					var iid = $(this).attr('data-iid');
					$.ajax({
						  url: '@@fetch-edit-data',
						  dataType: 'json',
						  data: {'iid': iid},
						  success: function (data) {
							  alert(data);
						  }
					});
			    });				
			},
			"oLanguage": {
				"sSearch": "Alles durchsuchen:"
			}		
		});
		$("#pfgsoupdata tfoot input").keyup( function () {
			/* Filter on the column (the index) of this element */
			oTable.fnFilter( this.value, $("#pfgsoupdata tfoot input").index(this) );
		} );		
		$("#pfgsoupdata tfoot input").each( function (i) {
			PFGSOUP_asInitVals[i] = this.value;
		} );
		
		$("#pfgsoupdata tfoot input").focus( function () {
			if ( this.className == "search_init" )
			{
				this.className = "";
				this.value = "";
			}
		} );		
		$("#pfgsoupdata tfoot input").blur( function (i) {
			if ( this.value == "" )
			{
				this.className = "search_init";
				this.value = PFGSOUP_asInitVals[$("#pfgsoupdata tfoot input").index(this)];
			}
		} );		
	});
})(jQuery);