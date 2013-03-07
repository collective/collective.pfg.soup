if (typeof(window['PFGSOUP']) == "undefined") PFGSOUP = {};

(function($) {

	$.extend(PFGSOUP, {
		asInitVals: new Array(),
		post: function(result, textStatus, jqXHR) {			
			var form = $('<form></form>');	
			
		    form.attr("method", "post");
		    form.attr("action", result.url);
	
		    $.each(result.data, function(key, value) {
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
		    document.cookie = c_name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/;';
		}

	});

	$(document).ready(function() {
		var url = $('#pfgsoupdata').attr('data-ajaxurl');
		var oTable = $('#pfgsoupdata').dataTable( {
			"bProcessing": true,
			"bServerSide": true,
			"sAjaxSource": url,
			"sPaginationType": "full_numbers",
			"bStateSave": true,
			"aaSorting": [],
			"aoColumnDefs": [
			     {"aTargets": [-1], 
			      "bSortable": false, 
			      "bSearchable": false,
			      "sWidth": "3em"
			     }
			],
			"fnDrawCallback" : function(oSettings) {
				$("#pfgsoupdata tbody a.pfgsoup-edit").click(function() {
					var iid = $(this).attr('data-iid');
					var url = $('#pfgsoupdata').attr('data-editurl');
					PFGSOUP.set_cookie('PFGSOUP_EDIT', iid);
					$.ajax({
						  url: url,
						  dataType: 'json',
						  data: {iid : iid},
						  success: PFGSOUP.post
					});
			    });
    			$("#pfgsoupdata tbody a.pfgsoup-log").prepOverlay({
					subtype: 'ajax'							
				});
    			$('#pfgsoupdata tbody a.pfgsoup-delete').click(function(){
    				/* TODO: nice jquerui modal dialog */
    				return confirm('Are you sure?');			
    			});    			
			},
			"oLanguage": {
		          "sUrl": "@@collective.js.datatables.translation"
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
		
		// below here: SOUP EDIT
		$("div.pfg-form form.fgBaseEditForm").before(function() {
			var iid = PFGSOUP.get_cookie('PFGSOUP_EDIT');
			if (iid==undefined) {
				return ''
			}
			var message = '<dl class="portalMessage info"><dt>Info</dt><dd>';
			message = message + "Form in Edit-Mode (ID "+iid+").";
			message = message + "</dd></dl>";
			message = $(message);
			return message;
		} );		
		$(window).unload(function(){
			if ($('table#pfgsoupdata').length != 0 || $('div.pfg-form form.fgBaseEditForm').length != 0)  {
				return;
			}
			PFGSOUP.del_cookie('PFGSOUP_EDIT');
		});
		$("#fg-base-edit").each(function() {
			var iid = PFGSOUP.get_cookie('PFGSOUP_EDIT');
			if (iid!=undefined) {
				return ''
			}			
			PFGSOUP.del_cookie('PFGSOUP_EDIT');
			$.ajax({
				  url: '@@pfgreeditdata',
				  dataType: 'json',
				  success: function (result, textStatus, jqXHR) {
					  if (result.status != 'ok') {
						  PFGSOUP.del_cookie('PFGSOUP_EDIT');
					      return;
					  }
					  PFGSOUP.set_cookie('PFGSOUP_EDIT', result.intid);
					  PFGSOUP.post(result, textStatus, jqXHR);
				  }					  
			});			
		});
		// end SOUP Edit
	});
})(jQuery);