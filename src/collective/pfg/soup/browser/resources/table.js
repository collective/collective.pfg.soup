if (typeof(window['PFGSOUP']) == "undefined") PFGSOUP = {};

(function($) {

	$.extend(PFGSOUP, {
		asInitVals: new Array(),
		post: function(data, textStatus, jqXHR) {
			var form = $('<form></form>');
			var path = $('#pfgsoupdata').attr('data-formurl');
	
		    form.attr("method", "post");
		    form.attr("action", path);
	
		    $.each(data, function(key, value) {
		        var field = $('<input type="hidden"></input>');
		        field.attr("name", key);
		        field.attr("value", value);
	
		        form.append(field);
		    });
		    $(document.body).append(form);
		    form.submit();
		},
		set_cookie: function (c_name, value) {
			var c_value = escape(value) + "; path=/;";
			document.cookie = c_name + "=" + c_value;
		},
		get_cookie: function(c_name) {
			var i, x, y, ARRcookies = document.cookie.split(";");
			for (i=0; i<ARRcookies.length; i++) {
				x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
				y = ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
				x = x.replace(/^\s+|\s+$/g,"");
				if (x==c_name) {
		            return unescape(y);
		        }
		    }
		},
		del_cookie: function (c_name)	{
		    document.cookie = c_name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
		}

	});

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
					var url = $('#pfgsoupdata').attr('data-editurl');
					PFGSOUP.set_cookie('PFGSOUP_EDIT', iid, 1);
					$.ajax({
						  url: url,
						  dataType: 'json',
						  data: {iid : iid},
						  success: PFGSOUP.post
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
			PFGSOUP.asInitVals[i] = this.value;
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
				this.value = PFGSOUP.asInitVals[$("#pfgsoupdata tfoot input").index(this)];
			}
		} );	
		$("div.pfg-form form.fgBaseEditForm").before(function() {
			var iid = PFGSOUP.get_cookie('PFGSOUP_EDIT');
			if (iid=="undefined") {
				return ''
			}
			var message = '<dl class="portalMessage info"><dt>Info</dt><dd>';
			message = message + "Form in Edit-Mode (ID "+iid+").";
			message = message + "</dd></dl>";
			message = $(message);
			return message;
		} );
		
	});
})(jQuery);