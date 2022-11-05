$(function () {
    $('#detailed').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var modal = button.data('modal')
        if (modal === "news") {
            var news = button.data('news')
            var description = button.data('description')
            var modal = $(this)
            modal.find('.modal-news').text(news)
            modal.find('.modal-description').text(description)
        } else if (modal === "pact") {
            var branch = button.data('branch')
            var type = button.data('type')
            var staff = button.data('staff')
            var client = button.data('client')
            var term = button.data('term')
            var ssum = button.data('ssum')
            var conclusion = button.data('conclusion')
            var modal = $(this)
            modal.find('.modal-branch').text(branch)
            modal.find('.modal-type').text(type)
            modal.find('.modal-staff').text(staff)
            modal.find('.modal-client').text(client)
            modal.find('.modal-term').text(term)
            modal.find('.modal-ssum').text(ssum)
            modal.find('.modal-conclusion').text(conclusion)
        } else if (modal === "staff") {
            var button = $(event.relatedTarget)
            var role = button.data('role')
            var telephone = button.data('telephone')
            var birthday = button.data('birthday')
            var branch = button.data('branch')
            var post = button.data('post')
            var fio = button.data('fio')
            var address = button.data('address')
            var logpass = button.data('logpass')
            var email = button.data('email')
            var date = button.data('date')
            var modal = $(this)
            modal.find('.modal-role').text(role)
            modal.find('.modal-telephone').text(telephone)
            modal.find('.modal-birthday').text(birthday)
            modal.find('.modal-branch').text(branch)
            modal.find('.modal-post').text(post)
            modal.find('.modal-fio').text(fio)
            modal.find('.modal-address').text(address)
            modal.find('.modal-logpass').text(logpass)
            modal.find('.modal-email').text(email)
            modal.find('.modal-date').text(date)
        }

    });

    $('.nav-link').each(function () {
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
        let link = this.href;
        if (location.includes(link) && link !== 'http://127.0.0.1:8000/') {
            $(this).addClass('active')
        }
    });

})