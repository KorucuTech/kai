// Copyright (c) 2024, Kemal Korucu and contributors
// For license information, please see license.txt

// frappe.ui.form.on("KAI LLM", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("KAI LLM", {
    load_settings_template(frm) {
        console.log(frm);
        if (frm.doc.settings=='{}' || frm.doc.settings=='') {
            if (frm.doc.llm_provider=='Ollama') {
                template = `{
    "base_url": "http://localhost:11434",
    "model": "llama3",                  
    "num_ctx": 2048,
    "num_gpu": 1,
    "repeat_last_n": 64,
    "repeat_penalty": 1.1,
    "temperature": 0,
    "top_k": 40,
    "top_p": 0.9,
    "timeout": 180,
}`;
                frm.set_value("settings",template);
            } else if (frm.doc.llm_provider=='GroqCloud') {
                template = `{
    "groq_api_key": "gsk_...",
    "groq_api_base": "",
    "model_name": "llama....",
    "model_kwargs" : {},
    "groq_proxy": "",
    "request_timeout": 180.0,
    "n": 1,
    "temperature": 0.7,
    "max_tokens": 1024,
    "top_p": 1,
    "streaming": false,
    "max_retries": 2,
    "verbose": false
}`;
                frm.set_value("settings",template);
            } else if (frm.doc.llm_provider=='AWS Bedrock') {
                template = `{

}`
                frm.set_value("settings",template);
            } else if (frm.doc.llm_provider=='OpenAI') { 
                template = `{

}`
                frm.set_value("settings",template);
            } else {
                frappe.msgprint("Unkown LLM Provider");
            }
        } else {
            frappe.msgprint("Settings Not Empty!");
        }
    }
});