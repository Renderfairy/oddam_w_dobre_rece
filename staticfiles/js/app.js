document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          if (this.currentStep === 2) {
            let ids = get_checked_category_checkboxes();
            if (ids.length < 1) {
              alert('Wybierz przynajmniej jedną ktegorię!');
              return;
            }
            let params = new URLSearchParams();
            ids.forEach(id => params.append("category_ids", id));
            let address = '/donation?' + params.toString();
            fetch(address)
                .then(response => response.text())
                .then(data => document.getElementById("inst").innerHTML = data)
          }

          if (this.currentStep === 5 ) {
            document.querySelector('#summary_1').firstElementChild.lastElementChild.innerText = document.querySelector('#id_quantity').value + ' worki';
            if (document.querySelector('#id_quantity').value.length === 0) {
              alert('Podaj ilosć worków w kroku 2/5!')
            }
            let second_li = document.querySelector('#summary_1').lastElementChild.lastElementChild;
            let organization = document.querySelector('input[name="organization"]:checked');
            if (organization == null) {
              alert('Wybierz organizację w kroku 3/5')
            }
            document.querySelector('#street').innerText = document.querySelector('#id_address').value;
            if (document.querySelector('#id_address').value.length === 0) {
              alert('Podaj ulicę, numer domu oraz mieszkania w kroku 4/5!')
            }
            document.querySelector('#city').innerText = document.querySelector('#id_city').value;
            if (document.querySelector('#id_zip_code').value.length === 0) {
              alert('Wpisz miasto!')
            }
            document.querySelector('#postal').innerText = document.querySelector('#id_zip_code').value;
            if (document.querySelector('#id_zip_code').value.length === 0) {
              alert('Wpisz kod pocztowy!')
            }
            document.querySelector('#phone').innerText = document.querySelector('#id_phone_number').value;
            if (document.querySelector('#id_phone_number').value.length === 0) {
              alert('Wpisz numer telefonu!')
            }
            document.querySelector('#pickup-date').innerText = document.querySelector('#id_picup_date').value;
            if (document.querySelector('#id_picup_date').value.length === 0) {
              alert('Wybierz datę odbioru!')
            }
            document.querySelector('#pickup-time').innerText = document.querySelector('#id_picup_time').value;
            if (document.querySelector('#id_picup_time').value.length === 0) {
              alert('Wybierz godzinę odbioru!')
            }
            document.querySelector('#pickup-comment').innerText = document.querySelector('#id_picup_comment').value;
            if (document.querySelector('#id_picup_comment').value.length === 0) {
              alert('Dodaj komentrz dla kuriera!')
            }
            if (organization != null) {
              second_li.innerText = organization.nextElementSibling.nextElementSibling.firstElementChild.innerText;
            }
          }

          this.updateForm();
        });
      });

      function get_checked_category_checkboxes() {
        const checkboxes = document.querySelectorAll('input[name="categories"]:checked');
        const ids = [];
        checkboxes.forEach(checkbox => ids.push(checkbox.value));
        // console.log(ids);
        return ids
      }

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

     this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();

      let categories = document.querySelectorAll('input[name="categories"]:checked');

      let quantity = document.querySelector('#id_quantity').value;
      let organization = document.querySelector('input[name="organization"]:checked').value;
      let address = document.querySelector('#id_address').value;
      let city = document.querySelector('#id_city').value;
      let postal = document.querySelector('#id_zip_code').value;
      let phone = document.querySelector('#id_phone_number').value;
      let date = document.querySelector('#id_picup_date').value;
      let time = document.querySelector('#id_picup_time').value;
      let comment = document.querySelector('#id_picup_comment').value;
      const formData = new FormData()
      formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
      categories.forEach(data => formData.append('categories', data.value));
      formData.append('quantity', quantity);
      formData.append('institution', organization);
      formData.append('address', address);
      formData.append('city', city);
      formData.append('zip_code', postal);
      formData.append('phone_number', phone);
      formData.append('picup_date', date);
      formData.append('picup_time', time);
      formData.append('picup_comment', comment);
      // for (let item of formData) {
      //   console.log(item[0], item[1])
      // }
      fetch('donation', {
        method: 'POST',
        body: formData,
      })
          .then(data => {
            console.log('Success', data)
            document.getElementById('form-information').innerHTML = '<div class="slogan container container--90">\n' +
                '        <h2>\n' +
                '            Dziękujemy za przesłanie formularza Na maila prześlemy wszelkie\n' +
                '            informacje o odbiorze.\n' +
                '        </h2>\n' +
                '    </div>'
          });
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
