tinymce.init({
					selector:   "textarea",
					width:      '100%',
					height:     270,
					plugins: [
      'advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker',
      'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
      'save table contextmenu directionality emoticons template paste textcolor'
    ],
    
    toolbar: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media fullpage | forecolor backcolor emoticons',
					statusbar:  true,
					menubar:    true
				});

			// Prevent bootstrap dialog from blocking focusin
			$(document).on('focusin', function(e) {
			if ($(e.target).closest(".mce-window").length) {
				//e.stopImmediatePropagation();
				}
			});

			$('#open').click(function() {
			$("#dialog").dialog({
				width: 1000,
				modal: true
			});
			});
			
			
/*$(document).ready(function() {
	$('#save').click(function() {
    $.ajax({
        method: 'POST',
        url: '^addLesson/{{course.course_name}}$',
        data: {'lesson_text': lesson_text},
        success: function (data) {
              var lesson_text = tinyMCE.get('content'); 
        },
        error: function (data) {
             
        }
    });
	
	function ajaxLoad() {
    var lesson_text = tinyMCE.get('content');

    ed.setProgressState(1); 
    window.setTimeout(function() {
        ed.setProgressState(0); 
        ed.setContent('lesson_text');
    }, 3000);
}*/

function ajaxSave() {
    var lesson_text = tinyMCE.get('content');

    
    ed.setProgressState(1); 
    window.setTimeout(function() {
        lesson_text.setProgressState(0); 
        alert(lesson_text.getContent());
    }, 3000);
}
	
	