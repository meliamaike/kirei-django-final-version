document.addEventListener('DOMContentLoaded', function() {
    var today = new Date();
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      themeSystem: 'standard',
      height: 'auto',
      contentHeight: 'auto',
      aspectRatio: 1.5,
      headerToolbar: {
        start: '',
        center: 'title',
        end: 'prev,next today'
      },
      buttonText: {
        prev: '<',
        next: '>',
        today: 'Hoy',
        month: 'Mes',
        week: 'Semana',
        day: 'Día',
        list: 'Agenda'
      },
      hiddenDays: [0,6],
      initialView: 'dayGridMonth',
      editable: false,
      events: 'booking/calendar/',
      dateClick: function(info) {
        window.location.href = '/booking/slot/?date=' + info.dateStr;
      },
      // Set locale to Spanish
      locale: 'es',
      // Disable dates before today
      validRange: {
        start: today
      }
    });

    calendar.render();
  });