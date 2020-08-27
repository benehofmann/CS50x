$(function(){
  $('[data-toggle="tooltip"]').tooltip();

  // Generate Event-Listeners for the Form-Fields
    var marital = document.getElementById("marital_status");
    var calculateButton = document.getElementById("calculateButton")
    var income_last_year = document.getElementById("income_last_year");
    var contractPartnerYes = document.getElementById("partner_yes");
    var contractPartnerNo = document.getElementById("partner_no");
    var showCalculation = document.getElementById("showCalculation");
    var resetButton = document.getElementById("resetButton");
    var pdfButton = document.getElementById("pdfButton");
    marital.addEventListener("change", togglePartner);
    calculateButton.addEventListener("click", calculatePayment);
    income_last_year.addEventListener("change", round);
    contractPartnerYes.addEventListener("change", disablePartnerInput);
    contractPartnerNo.addEventListener("change", disablePartnerInput);
    showCalculation.addEventListener("click", showDetails);
    resetButton.addEventListener("click", resetForm);
    pdfButton.addEventListener("click", createPDF);


    function resetForm() {
        $("#marital_status").val($("#marital_status option:first").val());
        $("#children_overall").val($("#children_overall option:first").val());
        resetUserChildren();
        resetPartnerChildren();
        $("#born_before_2008_user").val($("#born_before_2008_partner option:first").val());
        $(".data-partner-container").hide();
        $(".radiocheck").prop("checked", false);
        $("#payment_amount").val($("#payment_amount option:first").val());
        $("#payment_method_options").val($("#payment_method_options option:first").val());
        $("#income_last_year").val("");
        $("#payment_table").hide();
        $("#pdfButton").hide();
        $(".output").hide();
    }

    function showDetails() {
        $("#payment_table").show();
        $("#pdfButton").show();
    }

    function round() {
        $("#income_last_year").val(Math.ceil(parseFloat(income_last_year.value).toFixed(2)) );

    }

    function resetUserChildren() {
            $("#born_before_2008_user").val($("#born_before_2008_partner option:first").val());
            $("#born_2008_or_later_user").val($("#born_2008_or_later_partner option:first").val());
    }

    function resetPartnerChildren() {
            $("#born_before_2008_partner").val($("#born_before_2008_partner option:first").val());
            $("#born_2008_or_later_partner").val($("#born_2008_or_later_partner option:first").val());
    }

   function togglePartner(){


    switch($("#marital_status option:selected").val()) {
        case "single":
            disablePartnerFields();
            resetPartnerChildren();
            break;
        case "married":
            enablePartnerFields();
            break;
        case "widowed":
            disablePartnerFields();
            resetPartnerChildren();
            break;
    }
   }

   function disablePartnerInput() {
       if($("#partner_yes").is(":checked")) {$(".partner-input-fields").show(); }

        if($("#partner_no").is(":checked")) {$(".partner-input-fields").hide(); }
   }

   function disablePartnerFields() {

            $(".data-partner-container").hide();
            $(".data-partner").prop("checked", false);


   }

   function enablePartnerFields() {

        $(".data-partner-container").css("display", "flex");




   }

    function resetColors() {
        $("#marital_status").css("background-color", "white")
        $(".childinfo").css("background-color", "white");
        $(".childinfo").css("background-color", "white");
        $("#income_last_year").css("background-color", "white");
        $(".partner_data").css("background-color", "white");
        $("#beneficiary_you_direct_container").css("background-color","white");
        $("#beneficiary_you_indirect_container").css("background-color","white");
        $("#beneficiary_partner_direct_container").css("background-color", "white");
        $("#beneficiary_partner_indirect_container").css("background-color", "white")
    }

    function createPDF() {


    //get the data to write to the pdf
    var today = new Date();
    var income = $("#income").text()
    var income_4_percent = $("#4_percent_income").text();
    var basic_subsidiy = "175 EUR"
    var partner_subsidy = $("#partner_subsidy").text();
    var child_subsidy_before_2008 = $("#child_before_2008").text()
    var child_subsidy_2008_or_later = $("#child_2008_or_later").text();
    var final_result = $("#final_result").text();

    var output = "Income " + income + "\n" + "\n"
                + "4% of your income " + income_4_percent + "\n" + "\n"
                + "- basic subsidy " + "175 EUR" + "\n" + "\n"
                + "- partner subsidy " + partner_subsidy + "\n" + "\n"
                + "- child subsidy (born before 2008) " + child_subsidy_before_2008 + "\n" + "\n"
                + "- child subsidy (born 2008 or later) " + child_subsidy_2008_or_later + "\n" + "\n"
                + "Final Result " + final_result + "\n\n\n\n"
                + String(today) + "\n\n"
                + "created via the Riester-Payment-Calculator as part of the final Web-Project";


    const { jsPDF } = window.jspdf;

    const doc = new jsPDF();
    doc.text(output, 10, 10);
    doc.save("Riester_Payment.pdf");
    }


   function calculatePayment() {


        //preset get all field values
        var marital_status = $("#marital_status option:selected").val();
        var beneficiary_you = $("input:radio[name='beneficiary_you']:checked").val();
        var has_partner_contract = $("input:radio[name='contract_partner']:checked").val();
        var payment_method = $("#payment_method_options").val();
        var payment_amount = $("#payment_amount").val();
        var beneficiary_partner = $("input:radio[name='beneficiary_partner']:checked").val();

        //check if marital is filled
        if(typeof marital_status === "undefined" || marital_status == "Choose...") {
            alert("Choose marital first");
            $("#marital_status").css("background-color", "yellow")
            return;
        }

       //check if beneficiary is filled
        if(typeof beneficiary_you  === "undefined" && typeof beneficiary_partner ==="undefined") {
            alert("Choose beneficiary")
            $("#beneficiary_you_direct_container").css("background-color","yellow");
            $("#beneficiary_you_indirect_container").css("background-color","yellow");
            $("#beneficiary_partner_direct_container").css("background-color", "yellow");
            $("#beneficiary_partner_indirect_container").css("background-color", "yellow")
            return;
        }


        if(typeof beneficiary_you  === "undefined") {
            alert("Choose beneficiary")
            $("#beneficiary_you_direct_container").css("background-color","yellow");
            $("#beneficiary_you_indirect_container").css("background-color","yellow");
            return;
        }


        if(marital_status == "married" && typeof beneficiary_partner === "undefined" && typeof has_partner_contract === "undefined" || marital_status == "married" && typeof beneficiary_partner === "undefined" &&  has_partner_contract == "yes") {
            alert("Choose beneficiary for your partner")
            $("#beneficiary_partner_direct_container").css("background-color", "yellow");
            $("#beneficiary_partner_indirect_container").css("background-color", "yellow")
            return;
        }
       //reset color
        resetColors();



             //no of children
        var no_Of_Children = $("#children_overall").val();
        var children_before_2008_user = parseInt($("#born_before_2008_user").val());
        isNaN(children_before_2008_user) == true ? children_before_2008_user = 0 : parseInt($("#born_before_2008_user").val());
        var children_after_2008_user = parseInt($("#born_2008_or_later_user").val());
        isNaN(children_after_2008_user) == true ? children_after_2008_user = 0 : parseInt($("#born_2008_or_later_user").val());
        var children_before_2008_partner = parseInt($("#born_before_2008_partner").val());
        isNaN(children_before_2008_partner) == true ? children_before_2008_partner = 0 : parseInt($("#born_before_2008_partner").val());
        var children_after_2008_partner = parseInt($("#born_2008_or_later_partner").val());
        isNaN(children_after_2008_partner) == true ? children_after_2008_partner = 0 : parseInt($("#born_2008_or_later_partner").val());
        var child_subsidy_before_2008 =  (children_before_2008_user + children_before_2008_partner) * 185;
        var child_subsidy_2008_or_later =  (children_after_2008_user + children_after_2008_partner) * 300;

            //income
        var income = parseInt($("#income_last_year").val());
        var income_4_percent = (income / 100) * 4;
        income_4_percent > 2100 ? income_4_percent = 2100 : income_4_percent = income_4_percent;


        var needed_payment = Math.ceil(parseFloat(income_4_percent - 175 - child_subsidy_before_2008 - child_subsidy_2008_or_later).toFixed(3) * 100) / 100;

        //check case 1 single/widowed & indirect


        if(beneficiary_you == "indirect" && marital_status == "single" || beneficiary_you == "indirect" && marital_status == "widowed") {
            alert("Single and indirectly beneficiary. You are not eligble for Riester. Sorry !")
            return;
        }

        //check case 2 married & indirect & partner has no contract
        if(beneficiary_you == "indirect" && marital_status == "married" && has_partner_contract == "no" || beneficiary_you == "indirect" && marital_status == "married" && has_partner_contract == "no") {
             alert("You are indirectly beneficiary and your partner hasn`t a Riester-Contract. You are not eligble for Riester. Sorry !")
            return;
        }

        //check case 3 married & indirect you & partner direct and has a contract, only 60,00 EUR needed
        if(beneficiary_you == "indirect" && marital_status == "married" && has_partner_contract == "yes" && beneficiary_partner == "direct") {
             $("#needed_payment").html("Only "+ 60 + " EUR needed to get full subsidy.");
            if(payment_amount == "full subsidy") {
                switch(payment_method) {
                    case "monthly":
                        $("#payment_method").html("That is 5 EUR per month.");
                        break;

                    case "quarterly":
                        $("#payment_method").html("That is 15 EUR per quarter.");
                        break;

                    case "half-yearly":
                        $("#payment_method").html("That is 30 EUR per half-year.");
                        break;

                    case "annual":
                        $("#payment_method").html("That is 60 EUR per year.");
                        break;
                 }
                 $(".output").show();
                 $("#showCalculation").hide()
                 return;
            }
            if(payment_amount == "maximum") {
                switch(payment_method) {
                    case "monthly":
                        $("#payment_method").html("160,42" + " EUR per month as maximal subsidized payment");
                        break;

                    case "quarterly":
                        $("#payment_method").html("481,25" + " EUR per quarter as maximal subsidized payment");
                        break;

                    case "half-yearly":
                        $("#payment_method").html("962,50" + " EUR per half-year as maximal subsidized payment");
                        break;

                    case "annual":
                        $("#payment_method").html("1925" +  " EUR per year as maximal subsidized payment");
                        break;
                 }
                 $(".output").show();
                 $("#showCalculation").hide()
                 return;
            }


        }

        //check case 4 married & partner_contract_yes both indirect
        if(beneficiary_you == "indirect" && marital_status == "married" && has_partner_contract == "yes" && beneficiary_partner =="indirect" || beneficiary_you == "indirect" && marital_status == "married" && has_partner_contract == "yes" && beneficiary_partner =="indirect") {
             alert("You are both indirectly beneficiary. You are not eligble for Riester. Sorry !")
            return;
        }


        //check case 5 single + direct or both partners direct

        //check if children numbers are equal
        if(no_Of_Children != children_before_2008_user + children_after_2008_user + children_before_2008_partner + children_after_2008_partner) {
            $(".childinfo").css("background-color", "yellow");
            alert("Please fill child data");
            return;
        }

        //check for valid income
        if(!$("#income_last_year").val()) {
            $("#income_last_year").css("background-color", "yellow")
            alert("Please fill income")
        }

        if(beneficiary_you == "direct" && marital_status == "single" || beneficiary_you == "direct" && marital_status == "widowed" || marital_status == "married" && beneficiary_you == "direct" && beneficiary_partner == "direct") {

        //change table data
        $("#income").html(income + " EUR");

        if(income_4_percent > 2100) {
            $("#4_percent_income").html("2100" + " EUR");
            income_4_percent = 2100;
        } else {
            $("#4_percent_income").html(income_4_percent + " EUR");
        }

        $("#basic_subsidy").html("175 EUR");
        $("#partner_subsidy").html("0 EUR");
        $("#child_before_2008").html(child_subsidy_before_2008 + " EUR");
        $("#child_2008_or_later").html(child_subsidy_2008_or_later + " EUR");

        //check payment for subsidy
        needed_payment = Math.ceil(parseFloat(income_4_percent - 175 - child_subsidy_before_2008 - child_subsidy_2008_or_later).toFixed(3) * 100) / 100;
            if(needed_payment < 60) {
                $("#final_result").html(needed_payment + " EUR. So at least 60 EUR is needed to get full subsidy")
                needed_payment = 60;
            }
        $("#needed_payment").html((needed_payment < 60) ? "Only "+ 60 + " EUR to get full subsidy" : "You need to pay " + needed_payment + " EUR in a year to get full subsidy");
        $("#final_result").html(needed_payment + " EUR")

        // get payment with payment method
        if(payment_amount == "full subsidy") {

        switch(payment_method) {
            case "monthly":
                $("#payment_method").html("That is " + Math.ceil((parseFloat(needed_payment / 12).toFixed(3) * 100)) / 100 + " EUR per month");
                break;

            case "quarterly":
                $("#payment_method").html("That is " + Math.ceil((parseFloat(needed_payment / 4).toFixed(3) * 100)) / 100 + " EUR per quarter");
                break;

            case "half-yearly":
                $("#payment_method").html("That is " + Math.ceil((parseFloat(needed_payment / 2).toFixed(3) * 100)) / 100 + " EUR per half-year");
                break;

            case "annual":
                $("#payment_method").html("That is " + Math.ceil((parseFloat(needed_payment / 1).toFixed(3) * 100)) / 100 + " EUR per year");
                break;
        }
        $(".output").show();

        return


            }

        if(payment_amount == "maximum") {
            var maximum = 2100 - 175 - child_subsidy_before_2008 - child_subsidy_2008_or_later;
            switch(payment_method) {
                case "monthly":
                    $("#payment_method").html(Math.ceil((parseFloat(maximum / 12).toFixed(3) * 100)) / 100 + " EUR per month as maximal subsidized payment");
                    break;
                case "quarterly":
                    $("#payment_method").html(Math.ceil((parseFloat(maximum / 4).toFixed(3) * 100)) / 100 + " EUR per quarter as maximal subsidized payment");
                    break;
                case "half-yearly":
                    $("#payment_method").html(Math.ceil((parseFloat(maximum / 2).toFixed(3) * 100)) / 100 + " EUR per half-year as maximal subsidized payment");
                    break;
                case "annual":
                    $("#payment_method").html(Math.ceil((parseFloat(maximum).toFixed(3) * 100)) / 100 + " EUR per year as maximal subsidized payment");
                    break;
            }
            $(".output").show();
            return;
        }


        }




        //case 6 married , user direct, parner indirect
        if(no_Of_Children != children_before_2008_user + children_after_2008_user + children_before_2008_partner + children_after_2008_partner) {
            $(".childinfo").css("background-color", "yellow");
            alert("Please fill child data");
            return;
        }

        //check for valid income
        if(!$("#income_last_year").val()) {
            $("#income_last_year").css("background-color", "yellow")
            alert("Please fill income")
        }

        if(beneficiary_you == "direct" && marital_status == "married" && beneficiary_partner == "indirect"  && has_partner_contract == "yes") {
            //change table data
            $("#income").html(income + " EUR");

            if(income_4_percent > 2100) {
                $("#4_percent_income").html("2100" + " EUR");
                income_4_percent = 2100;
            } else {
                $("#4_percent_income").html(income_4_percent + " EUR");
            }

            $("#basic_subsidy").html("175 EUR")
            $("#partner_subsidy").html("175 EUR")
            $("#child_before_2008").html(child_subsidy_before_2008 + " EUR");
            $("#child_2008_or_later").html(child_subsidy_2008_or_later + " EUR");

            //assign new needed payment; user gets partner subsidy
            needed_payment = needed_payment - 175;
            //check payment for subsidy
            if(needed_payment < 60) {
                $("#final_result").html(needed_payment + " EUR. So at least 60 EUR is needed to get full subsidy")
                needed_payment = 60;
            }

            $("#needed_payment").html((needed_payment = 60) ? "Only "+ 60 + " EUR to get full subsidy" : "You need to pay " + needed_payment + " EUR in a year to get full subsidy");

        // get payment with payment method
        if(payment_amount == "full subsidy") {

        switch(payment_method) {
            case "monthly":
                $("#payment_method").html("That is " + Math.ceil((parseFloat(needed_payment / 12).toFixed(3) * 100)) / 100 + " EUR per month");
                break;

            case "quarterly":
                $("#payment_method").html("That is " + Math.ceil((parseFloat(needed_payment / 4).toFixed(3) * 100)) / 100 + " EUR per quarter");
                break;

            case "half-yearly":
                $("#payment_method").html("That is " + Math.ceil((parseFloat(needed_payment / 2).toFixed(3) * 100)) / 100 + " EUR per half-year");
                break;

            case "annual":
                $("#payment_method").html("That is " + Math.ceil((parseFloat(needed_payment / 1).toFixed(3) * 100)) / 100 + " EUR per year");
                break;
        }
        $("#final_result").html(needed_payment + " EUR in a year.")
        $(".output").show();
        return


            }

        if(payment_amount == "maximum") {
            var maximum = 2100 - 175 - 175 - child_subsidy_before_2008 - child_subsidy_2008_or_later;

            switch(payment_method) {
                case "monthly":
                    $("#payment_method").html(Math.ceil((parseFloat(maximum / 12).toFixed(3) * 100)) / 100 + " EUR per month as maximal subsidized payment");
                    break;
                case "quarterly":
                    $("#payment_method").html(Math.ceil((parseFloat(maximum / 4).toFixed(3) * 100)) / 100 + " EUR per quarter as maximal subsidized payment");
                    break;
                case "half-yearly":
                    $("#payment_method").html(Math.ceil((parseFloat(maximum / 2).toFixed(3) * 100)) / 100 + " EUR per half-year as maximal subsidized payment");
                    break;
                case "annual":
                    $("#payment_method").html(Math.ceil((parseFloat(maximum).toFixed(3) * 100)) / 100 + " EUR per year as maximal subsidized payment");
                    break;
            }
            $(".output").show();
            return;
        }
        }

//case 7 married, partner no contract, user direct

   }
});

