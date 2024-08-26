

const filters_operators = document.getElementById('filters_operators')
const filters_product = document.getElementById('filters_product')
const filters_statuses = document.getElementById('filters_statuses')
const leads_grid = document.querySelector('.leads_grid')

var date_changed = false

$(function () {
   $(document.getElementById("datepicker")).datepicker({ firstDay: 1 });
});


function get_date_str() {
    
    var dateObject = $('#datepicker').datepicker('getDate');
    var day = dateObject.getDate();
    var month = dateObject.getMonth() + 1;
    if (month < 10) month = `0${month}`
    var year = dateObject.getFullYear();
    var date_str = `${day}/${month}/${year}`
    return date_str
}


function getStatus(status) {
    const styleDict = {
        'New': 'text-blue-400',
        'Refused': 'text-red-400',
        'Approved': 'text-green-400',
        'Need approved': 'text-yellow-400'
    };
  
    const html = `<p class="${styleDict[status]}">${status}</p>`;
    return html;
}

async function filtrate_leads() {
    date_str = get_date_str()
    if (!date_changed) date_str = 'All'
    
    let request = await fetch(`${window.location.origin}/api/leads/get?date=${date_str}&operator=${filters_operators.value}&product=${filters_product.value}&status=${filters_statuses.value}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    let data = await request.json();
    
    var leads = data.leads
    leads_grid.innerHTML = ''
    if (leads.length == 0) return
    for (let i = 0; i < leads.length; i++) {
        let avatar_request = await fetch(`${window.location.origin}/api/operator/avatar/?pk=${leads[i].operator}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })

        let request_datas = await avatar_request.json()
        let lead_status = getStatus(leads[i].status)
        avatar = request_datas.avatar

        leads_grid.innerHTML += `
        <div class="grid grid-cols-12 bg-white p-4 my-2  gap-3 items-center rounded-md"
                     x-data="{ open: false }">

                    <div class="col-span-1 rounded-full">
                        <img class="rounded-full" src="${avatar}" alt="">
                    </div>

                    <div class="col-span-3">
                        <h5>
                            ${leads[i].name}
                        </h5>
                    </div>

                    <div class="col-span-2">
                                <span>
                                    Date:
                                </span>
                        <p>
                            ${leads[i].request_date}
                        </p>
                    </div>

                    <div class="col-span-2">
                                <span>
                                    Product:
                                </span>
                        <p>
                            ${leads[i].product}
                        </p>
                    </div>

                    <div class="col-span-2">
                                <span>
                                    Status:
                                </span>
                            ${lead_status}
                    </div>

                    <div x-on:click="open = true"
                         class="col-span-2 cursor-pointer items-center hover:text-green-500 transition-all">
                        <p class="inline-block">
                            Details
                        </p>
                        <i class="fa-solid fa-arrow-right-long"></i>
                    </div>

                    <div x-cloak x-show="open" x-transition:enter="transition ease-out duration-300"
                         x-transition:enter-start="opacity-0 scale-90"
                         x-transition:enter-end="opacity-100 scale-100"
                         x-transition:leave="transition ease-in duration-300"
                         x-transition:leave-start="opacity-100 scale-100"
                         x-transition:leave-end="opacity-0 scale-90"
                         class="fixed w-full h-screen top-0 left-0 z-10 bg-gray-300 opacity-90 blur-md"></div>

                    <div x-cloak x-show="open" x-transition:enter="transition ease-out duration-300"
                         x-transition:enter-start="opacity-0 scale-90"
                         x-transition:enter-end="opacity-100 scale-100"
                         x-transition:leave="transition ease-in duration-100"
                         x-transition:leave-start="opacity-100 scale-100"
                         x-transition:leave-end="opacity-0 scale-90"
                         class="translate-center p-4 rounded-md z-20 bg-whte">

                        <div>
                            <h5>${leads[i].name}</h5>
                        </div>

                        <div class="grid grid-cols-3 gap-2 mt-4 mb-2">
                            <input class="px-2 py-1 outline-cyan-400 lead_input_phone" id="${leads[i].id}" type="text" value="${leads[i].phone}">
                            <select class="px-2 py-1 outline-cyan-400 lead_input_status" name="" id="${leads[i].id}">
                                {% get_lead_detail_status_options lead.status as status_options %}{{status_options|safe}}
                                <!-- <option class="text-green-400" value="Approved">Approved</option>
                                <option class="text-blue-400" value="New" selected>New</option>
                                <option class="text-red-400" value="Refused">Refused</option>
                                <option class="text-yellow-400" value="Need approved">Need approved</option> -->
                            </select>

                            <select class="px-2 py-1 outline-cyan-400 lead_input_product" id="${leads[i].id}">
                                {% get_lead_detail_products_options lead.product as product_options %}{{product_options|safe}}
                                <!-- <option value="Lactos">Lactos</option>
                                <option value="Laditex">Laditex</option>
                                <option value="PerfectMan">PerfectMan</option> -->
                            </select>

                        </div>

                        <div class="grid grid-cols-3 gap-2 my-2 text-left">
                            <select class="px-2 py-1 outline-cyan-400 lead_input_address" id="${leads[i].id}" name="whatever" id="frm-whatever">
                                {% get_lead_detail_addresses_options lead.address as product_address %}{{product_address|safe}}
                                <!-- <option value="Toshkent shahri">Toshkent shahri</option>
                                <option value="Toshkent">Toshkent</option>
                                <option value="Sirdaryo">Sirdaryo</option>
                                <option value="Jizzax">Jizzax</option>
                                <option value="Samarqand">Samarqand</option>
                                <option value="Buxoro">Buxoro</option>
                                <option value="Navoiy">Navoiy</option>
                                <option value="Xorazim">Xorazim</option>
                                <option value="Qashqadaryo">Qashqadaryo</option>
                                <option value="Surxondaryo">Surxondaryo</option>
                                <option value="Farg'ona">Farg'ona</option>
                                <option value="Namangan">Namangan</option>
                                <option value="Andijon">Andijon</option>
                                <option value="Nukus shahri">Nukus shahri</option> -->
                            </select>
                            <h4 class="px-2 py-1 ">
                                Lead Came date:
                            </h4>
                            <h4 class="px-2 py-1 ">
                                ${leads[i].request_date}
                            </h4>
                        </div>

                        <!-- check if status approved show this -->

                        <!-- <div class="grid grid-cols-3 gap-2 my-2 text-left">
                            <p class="px-3 py-1 ">Sold</p>
                            <input class="px-2 py-1 outline-cyan-400 w-14" type="number" value="1">
                            <input class="px-2 py-1 outline-cyan-400" type="text" value="550 000 ">
                        </div> -->

                        <div class="grid grid-cols-3 gap-2 my-2 text-left">
                            <p class="px-3 py-1 ">Called</p>
                            <input class="px-2 py-1 outline-cyan-400 w-14 lead_input_soldcount" id="${leads[i].id}" type="number" value="1">
                            <input class="px-2 py-1 outline-cyan-400 lead_input_solddate" id="${leads[i].id}" type="date" value="">
                        </div>

                        <div>
                            <textarea class="w-full my-2 px-2 py-1 outline-cyan-400" name="" id=""
                                      placeholder="A..."></textarea>
                        </div>

                        <div class="flex justify-end my-2">
                            <div class="flex gap-2">
                                <button class="border bg-cyan-500 px-4 py-1 text-white text-md
                                                outline-none border-none hover:bg-cyan-400 transition-all
                                                shadow-cyan lead_edit_submit" id="${leads[i].id}">
                                    Edit
                                </button>
                                <button x-on:click="open = false" class="border bg-red-400 px-4 py-1 text-white text-md
                                                outline-none border-none hover:bg-red-500 transition-all
                                                shadow-red">
                                    Close
                                </button>
                            </div>
                        </div>

                    </div>


                </div>
        \n\n`
    }

}

$("#datepicker").datepicker({
onSelect: async function() {
    date_changed = true
    await filtrate_leads()
}
});

filters_operators.addEventListener('change', async () => {
    await filtrate_leads()
})

filters_product.addEventListener('change', async () => {
    await filtrate_leads()
})

filters_statuses.addEventListener('change', async () => {
    await filtrate_leads()
})