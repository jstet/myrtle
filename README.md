# Myrtle: a wise brachiosaurus
Just a fun project teach myself a bit to train and deploy LLMs. Myrtle is a GPT2 model finetuned on quotes by non male notable people. Find myrtle [here](https://github.com/jstet/myrtle). She only speaks every 5 seconds.

```
/----------------------------------------------------------------------------\
| The truth is that we are all flawed, and it takes courage to be ourselves. |
\----------------------------------------------------------------------------/
      \
       \
        \

    
         _
       .~O`,
      {__,  \
          \' \
           \  \
            \  \
             \  `._            __.__
              \    ~-._  _.==~~     ~~--.._
               \        '                  ~-.
                \      _-   -_                `.
                 \    /       }        .-    .  \
                  `. |      /  }      (       ;  \
                    `|     /  /       (       :   '\
                     \    |  /        |      /       \
                      |     /`-.______.\     |~-.      \
                      |   |/           (     |   `.      \_
                      |   ||            ~\   \      '._    `-.._____..----..___
                      |   |/             _\   \         ~-.__________.-~~~~~~~~~'''
                    .o'___/            .o______}
    
```

## Background

This project originated in the [CorrelAid](https://www.correlaid.org/) Slack workspace. A colleague, [Frie](https://www.frie.codes/), started a thread of recommending terminal tools that are useless but spark joy, for example [lolcat](https://github.com/busyloop/lolcat) combined with [cowsay](https://en.wikipedia.org/wiki/Cowsay). Cowsay basically draws a cow in your terminal and you can input text. From that I got the idea of somehow randomizing what the cow says and found [fortune](https://wiki.archlinux.org/title/Fortune), a program that prints random quotes from a local database. 

However, when trying fortune, I found some quotes to be pretty weird and even sexist. People have observed this before (read [this thread](https://wiki.archlinux.org/title/Fortune)). My next idea was to use an [API](https://github.com/lukePeavey/quotable) to retrieve a random quote by famous people from the internet. While working on a bash script to combine this API with cowsay, I researched cowsay flags and cow alternatives and again found some [weird stuff](https://github.com/schacon/cowsay/tree/master/cows) (take a look yourself if you are interested). Thats why I decided to use a wholesome, child friendly python package called [dinosay](https://github.com/MatteoGuadrini/dinosay) instead. The result was a bash script that uses a random quote from the internet as an input for dinosay. 

Not satisfied with this, I thought it would be funny to train a LLM to generate quotes that sound realistic. I wanted to learn how to this anyways so thats what I did. As training data, I used a large dataset of quotes found originally on GitHub and built for a paper (see below). As there are enough quotes of men circulating in the internet and LLMs [tend to be gender biased](https://towardsdatascience.com/gender-bias-in-gpt-2-acf65dc84bd8) I tried to only use quotes by non male people (I know that its not that easy). I also like to imagine Myrtle as a wise old female dinosaur. As you cant detect a persons gender through their name, I generated a list of names of non male notable people and only used quotes by authors with names in that list. I used this data to finetune a GPT2 model, because its small enough to not cost that much to run (no GPU necessary for inference) but good enough to sounds realistic. Processing and training was done remotely with [modal](https://modal.com/). 

This worked relatively good and I was suprised and had to laugh about how pseudo-wise some quotes sound. Try it yourself :)

## Usage in a terminal
I wrote a [simple bash script](https://github.com/jstet/dino_wisdom) to bring myrtles wisdom to your terminal. 

## Disclaimer
As myrtle is a finetuned GPT2 model, it is simarily biased. Information about this [here](https://huggingface.co/gpt2). Please bear in mind that I am not the one writing the quotes. While I tried to moderate the model output somewhat using various tools including a list of forbidden words, I cant guarantee non offensive text output.  

### Data Sources
- Laouenan, M., Bhargava, P., Eyméoud, J.B., Gergaud, O., Plique, G., & Wasmer, E. (2022). A cross-verified database of notable people, 3500BC-2018AD. Scientific Data, 9(1), 290.
- Goel, S., Madhok, R., & Garg, S. (2018). Proposing Contextually Relevant Quotes for Images. Advances in Information Retrieval. Springer. doi: 10.1007/978-3-319-76941-7_49
